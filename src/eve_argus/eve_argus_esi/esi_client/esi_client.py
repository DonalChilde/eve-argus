import asyncio
import logging
from collections.abc import Iterable, Sequence
from datetime import datetime, timedelta
from itertools import chain

import aiohttp

from eve_argus.eve_argus_esi.esi_cache.esi_cache_protocol import (
    CacheStatus,
    EsiCacheProtocol,
)
from eve_argus.eve_argus_esi.esi_schema.eve_openapi_protocol import EveOpenApiProtocol

from .models import (
    EsiAction,
    EsiPagedResponse,
    EsiRequest,
    EsiResponse,
    PagedAction,
    PagedRequest,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class QueueState:
    # queue counts
    processed: int = 0
    skipped: int = 0
    remaining: int = 0
    # error counts
    errors: int = 0
    error_resets_in: int = 0
    """from X-ESI-Error-Limit-Reset header"""
    errors_remaining: int = -1
    """from X-ESI-Error-Limit-Remain header"""
    error_resets_at: datetime | None = None
    error_messages: list[str] = []
    # State flags
    paged_error: bool = False
    stop_on_400: bool = False
    stop_operations: bool = False


async def wait_for_error_limit(name: str, queue_state: QueueState):
    if queue_state.errors_remaining == 0:
        logger.info(
            f"{name} - Waiting {queue_state.error_resets_in} seconds for error limit reset"
        )
        await asyncio.sleep(queue_state.error_resets_in)


def update_error_limits(
    headers: tuple[tuple[str, str | None], ...], queue_state: QueueState
):
    if response.headers.get("X-ESI-Error-Limit-Reset"):
        queue_state.error_resets_in = int(response.headers["X-ESI-Error-Limit-Reset"])
    if response.headers.get("X-ESI-Error-Limit-Remain"):
        queue_state.errors_remaining = int(response.headers["X-ESI-Error-Limit-Remain"])


class WorkerFactory:
    def __init__(self, max_workers: int) -> None:
        self.max_workers = max_workers
        self.max_paged_rate = max(int(max_workers / 2), 1)
        self.max_rate = max(self.max_workers - self.max_paged_rate, 1)

    def build_get_worker(
        self,
        name: str,
        queue: asyncio.Queue[EsiAction],
        session: aiohttp.ClientSession | None,
        cache: EsiCacheProtocol,
        queue_state: QueueState,
    ):
        """Cacheable, not paged"""

        async def get_worker():
            while True:
                action = await queue.get()
                await wait_for_error_limit(name, queue_state)
                queue_state.remaining = queue.qsize()
                if queue_state.stop_operations:
                    queue_state.skipped += 1
                    logger.info(
                        f"{name} skipping request {action.request.request_id} "
                        f"due to previous errors."
                    )
                    queue.task_done()
                    continue
                cache_status = cache.status(action.request.cache_key)
                etag = ""
                if cache_status is CacheStatus.HIT:
                    action.response = cache.get_response(action.request.cache_key)
                    queue_state.processed += 1
                    queue.task_done()
                    continue
                if cache_status is CacheStatus.STALE:
                    etag = cache.get_cache_metadata(action.request.cache_key).etag
                try:
                    response = await do_request(
                        esi_request=action.request,
                        session=session,
                        queue_state=queue_state,
                        etag=etag,
                    )
                    update_error_limits(response.headers, queue_state)
                    match response.status_code:
                        case 200:
                            metadata = cache.build_metadata(response)
                            cache.set(
                                cache_key=action.request.cache_key,
                                cache_metadata=metadata,
                                value=response,
                            )
                            action.response = cache.get_response(
                                action.request.cache_key
                            )
                            continue
                        case 304:
                            cache.update_304(action.request.cache_key, response)
                            action.response = cache.get_response(
                                action.request.cache_key
                            )
                            continue
                        case status if 400 <= status < 500:
                            queue_state.errors += 1
                            logger.error(
                                f"Client error {response.status_code} for request "
                                f"{action.request!r}"
                            )
                            action.response = response
                            if queue_state.stop_on_400:
                                queue_state.stop_operations = True
                            continue
                        case status if status >= 500:
                            queue_state.errors += 1
                            logger.error(
                                f"Server error {response.status_code} for request "
                                f"{action.request!r}"
                            )
                            # retry possible but out of scope for now.
                            action.response = response
                            continue
                        case _:
                            logger.error(
                                f"Unexpected error {response.status_code} for request "
                                f"{action.request!r}"
                            )
                            action.response = response
                            continue
                finally:
                    queue_state.processed += 1
                    queue.task_done()

        return get_worker

    # TODO functions for error limit data from headers. to save space.

    def build_paged_worker(
        self,
        name: str,
        queue: asyncio.Queue[PagedAction],
        session: aiohttp.ClientSession | None,
        queue_state: QueueState,
    ):
        async def paged_worker():
            while True:
                action = await queue.get()
                await wait_for_error_limit(name, queue_state)
                queue_state.remaining = queue.qsize()
                if queue_state.stop_operations:
                    queue_state.skipped += 1
                    logger.info(
                        f"{name} skipping paged request {action.request.request_id} "
                        f"due to previous errors."
                    )
                    queue.task_done()
                    continue
                try:
                    response = await do_paged_request(
                        paged_request=action.request,
                        session=session,
                        queue_state=queue_state,
                    )
                    update_error_limits(response.headers, queue_state)
                    if response.last_modified != action.request.parent_last_modified:
                        queue_state.paged_error = True
                        queue_state.errors += 1
                        queue_state.stop_operations = True
                        action.response = response
                    # TODO other stop conditions.
                    action.response = response
                finally:
                    queue_state.processed += 1
                    queue.task_done()

        return paged_worker


class PagedException(Exception):
    """Exception raised for errors in the ESI pagination.

    This error is raised when the last-modified header of a paged request does not
    match the parent last-modified header.
    """

    def __init__(self, message: str):
        super().__init__(message)


def do_actions(
    actions: Sequence[EsiAction], cache: EsiCacheProtocol, schema: EveOpenApiProtocol
):
    pass
    # do the actions.
    # check to see if the actions have pages.
    # - if they do, generate a list of PagedActions for each EsiAction that has pages.
    # - send each list of PagedActions to do_paged_actions.
    # - if PagedException is raised, try to repeat the originating EsiAction once.


def do_paged_actions(
    workers: int, actions: Sequence[PagedAction], worker_factory: WorkerFactory
) -> QueueState:
    if workers > worker_factory.max_paged_rate:
        _workers = worker_factory.max_paged_rate
        logger.info(f"Limiting workers from requested:{workers} to {_workers}")
    else:
        _workers = workers
    queue_state = asyncio.run(_run_paged_tasks(_workers, actions, worker_factory))
    return queue_state


async def _run_paged_tasks(
    workers: int, actions: Iterable[PagedAction], worker_factory: WorkerFactory
) -> QueueState:
    queue = asyncio.Queue[PagedAction]()
    for action in actions:
        queue.put_nowait(action)
    tasks = []
    async with aiohttp.ClientSession() as session:
        queue_state = QueueState()
        for i in range(1, workers + 1):
            task = asyncio.create_task(
                worker_factory.build_paged_worker(
                    name=f"PagedWorker-{i}",
                    queue=queue,
                    session=session,
                    queue_state=queue_state,
                )()
            )
            tasks.append(task)
            logger.debug(f"Starting paged worker {i} of {workers}")
        await queue.join()
    for task in tasks:
        task.cancel()
    return queue_state


async def do_request(
    esi_request: EsiRequest,
    session: aiohttp.ClientSession | None,
    queue_state: QueueState,
    etag: str = "",
) -> EsiResponse:
    pass

    # inject etag if not ""


async def do_paged_request(
    paged_request: PagedRequest,
    session: aiohttp.ClientSession | None,
    queue_state: QueueState,
) -> EsiPagedResponse:
    pass
    # TODO implement error timeout wait


def make_url(request: EsiRequest, base_url: str, schema: EveOpenApiProtocol) -> str:
    """Build the URL without query parameters for the given EsiRequest."""
    return schema.get_url(
        base_url=base_url,
        op_id=request.op_id,
        path_params=request.path_params,
        query_params=request.query_params,
        include_query=False,
    )


def do_actions_2(
    actions: Sequence[EsiAction],
    cache: EsiCacheProtocol,
    workers: int,
    stop_on_400: bool = False,
):
    """Perform the given ESI actions"""
    paged_actions = [x for x in actions if x.request.paged]
    not_paged_actions = [x for x in actions if not x.request.paged]


def do_paged_actions_2(
    actions: Sequence[EsiAction],
    cache: EsiCacheProtocol,
    workers: int,
    stop_on_400: bool = False,
):
    """Perform the given paged ESI actions."""
    cachable = [x for x in actions if x.request.cacheable]
    not_cachable = [x for x in actions if not x.request.cacheable]
    hit: list[EsiAction] = []
    missed: list[EsiAction] = []
    stale: list[EsiAction] = []
    retry: list[EsiAction] = []
    skipped: list[EsiAction] = []

    for action in cachable:
        match cache.status(action.request.cache_key):
            case CacheStatus.HIT:
                response = cache.get_response(action.request.cache_key)
                action.response = response
                hit.append(action)
            case CacheStatus.MISS:
                missed.append(action)
            case CacheStatus.STALE:
                stale.append(action)
            case _:
                raise ValueError("Invalid cache status")
    # Do the actions
    # handle remaining cachable actions
    for action in chain(missed, stale):
        if action.response is None:
            # handle None
            skipped.append(action)
            continue
        match action.response.status_code:
            case 200:
                metadata = cache.build_metadata(action.response)
                cache.set(
                    cache_key=action.request.cache_key,
                    cache_metadata=metadata,
                    value=action.response,
                )
            case 304:
                cache.update_304(action.request.cache_key, action.response)
            case status if 400 <= status < 500:
                # this might set stop inside the worker, no effect here
                pass
            case status if status >= 500:
                retry.append(action)
            case _:
                raise ValueError(
                    f"Unexpected response status code {action.response.status_code} for {action.response.real_url}"
                )
    for action in not_cachable:
        if action.response is None:
            # handle None
            skipped.append(action)
            continue
        match action.response.status_code:
            case 200:
                pass
            case status if 400 <= status < 500:
                # this might set stop inside the worker, no effect here
                pass
            case status if status >= 500:
                retry.append(action)
            case _:
                raise ValueError(
                    f"Unexpected response status code {action.response.status_code} for {action.response.real_url}"
                )
    if retry:
        # TODO retry once.
        pass


def paged_cachable(actions: Sequence[EsiAction], cache: EsiCacheProtocol):
    hit: list[EsiAction] = []
    missed: list[EsiAction] = []
    stale: list[EsiAction] = []
    retry: list[EsiAction] = []
    skipped: list[EsiAction] = []

    for action in actions:
        if not action.request.cacheable or not action.request.paged:
            logger.error(f"Action not cachable or not paged: {action!r}")
            raise ValueError("Action must be cachable and paged")
        match cache.status(action.request.cache_key):
            case CacheStatus.HIT:
                response = cache.get_response(action.request.cache_key)
                action.response = response
                hit.append(action)
            case CacheStatus.MISS:
                missed.append(action)
            case CacheStatus.STALE:
                stale.append(action)
            case _:
                raise ValueError("Invalid cache status")
    # TODO do the missed and stale actions
    # handle remaining cachable actions
    for action in chain(missed, stale):
        if action.response is None:
            # handle None
            skipped.append(action)
            continue
        match action.response.status_code:
            case 200:
                metadata = cache.build_metadata(action.response)
                cache.set(
                    cache_key=action.request.cache_key,
                    cache_metadata=metadata,
                    value=action.response,
                )
            case 304:
                cache.update_304(action.request.cache_key, action.response)
            case status if 400 <= status < 500:
                # this might set stop inside the worker, no effect here
                pass
            case status if status >= 500:
                retry.append(action)
            case _:
                raise ValueError(
                    f"Unexpected response status code {action.response.status_code} for {action.response.real_url}"
                )
    logger.info(f"Retrying {len(retry)} failed actions")
    for action in retry:
        # TODO retry once.
        pass
    for action in skipped:
def not_paged_cachable(actions:Sequence[EsiAction], cache: EsiCacheProtocol):
    hit: list[EsiAction] = []
    missed: list[EsiAction] = []
    stale: list[EsiAction] = []
    retry: list[EsiAction] = []
    skipped: list[EsiAction] = []

    for action in actions:
        if not action.request.cacheable or action.request.paged:
            logger.error(f"Action not cachable or paged: {action!r}")
            raise ValueError("Action must be cachable and not paged")
        match cache.status(action.request.cache_key):
            case CacheStatus.HIT:
                response = cache.get_response(action.request.cache_key)
                action.response = response
                hit.append(action)
            case CacheStatus.MISS:
                missed.append(action)
            case CacheStatus.STALE:
                stale.append(action)
            case _:
                raise ValueError("Invalid cache status")
    # TODO do the missed and stale actions
    # handle remaining cachable actions
    for action in chain(missed, stale):
        if action.response is None:
            # handle None
            skipped.append(action)
            continue
        match action.response.status_code:
            case 200:
                metadata = cache.build_metadata(action.response)
                cache.set(
                    cache_key=action.request.cache_key,
                    cache_metadata=metadata,
                    value=action.response,
                )
            case 304:
                cache.update_304(action.request.cache_key, action.response)
            case status if 400 <= status < 500:
                # this might set stop inside the worker, no effect here
                pass
            case status if status >= 500:
                retry.append(action)
            case _:
                raise ValueError(
                    f"Unexpected response status code {action.response.status_code} for {action.response.real_url}"
                )
    logger.info(f"Retrying {len(retry)} failed actions")
    for action in retry:
        # TODO retry once.
        pass