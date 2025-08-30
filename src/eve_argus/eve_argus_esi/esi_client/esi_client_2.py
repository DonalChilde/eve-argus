import asyncio
import logging
from collections import ChainMap
from collections.abc import Callable, Coroutine, Iterable, Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from itertools import chain
from typing import Any, Awaitable
from uuid import UUID

import aiohttp

from eve_argus.eve_argus_esi.esi_cache.esi_cache_protocol import (
    CacheStatus,
    EsiCacheProtocol,
)
from eve_argus.eve_argus_esi.esi_schema.eve_openapi_protocol import EveOpenApiProtocol
from eve_argus.eve_argus_esi.helpers.now_utc import now_utc

from .models import (
    EsiAction,
    EsiRequest,
    EsiResponse,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclass(slots=True)
class CacheCheck:
    hit: set[UUID]
    miss: set[UUID]
    stale: set[UUID]


class QueueState:
    # queue counts
    processed: int = 0
    skipped: int = 0
    remaining: int = 0
    # error counts
    errors: int = 0
    error_resets_in: int = 0
    """from X-ESI-Error-Limit-Reset header"""
    errors_remaining: int = 100
    """from X-ESI-Error-Limit-Remain header"""
    error_resets_at: datetime | None = None
    error_messages: list[str] = []
    # State flags
    paged_error: bool = False
    stop_on_400: bool = False
    stop_operations: bool = False


WorkerType = Callable[
    [str, asyncio.Queue[EsiAction], aiohttp.ClientSession, QueueState],
    Coroutine[Any, Any, Any],
]


async def wait_for_error_limit(name: str, queue_state: QueueState):
    if queue_state.errors_remaining < 10:
        logger.info(
            f"{name} - Waiting {queue_state.error_resets_in} seconds for error limit reset"
        )
        await asyncio.sleep(queue_state.error_resets_in)


def update_error_limits(
    headers: tuple[tuple[str, str | None], ...], queue_state: QueueState
):
    for header in headers:
        if header[0].lower() == "x-esi-error-limit-reset":
            queue_state.error_resets_in = int(header[1] or 0)
        elif header[0].lower() == "x-esi-error-limit-remain":
            queue_state.errors_remaining = int(header[1] or -1)


def build_worker() -> WorkerType:
    async def _worker(
        name: str,
        queue: asyncio.Queue[EsiAction],
        session: aiohttp.ClientSession,
        queue_state: QueueState,
    ):
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
            etag = ""
            try:
                match action.request.method.lower():
                    case "get":
                        response = await _do_get_request(
                            esi_request=action.request,
                            session=session,
                        )
                    case _:
                        raise ValueError(f"Unsupported method: {action.request.method}")
                update_error_limits(response.headers, queue_state)
            except Exception as e:
                logger.error(f"{name} - Error processing request: {e} for {action!r}")
                queue_state.stop_operations = True
            finally:
                queue_state.processed += 1
                queue.task_done()

    return _worker


async def _worker(
    name: str,
    queue: asyncio.Queue[EsiAction],
    session: aiohttp.ClientSession,
    queue_state: QueueState,
) -> None:
    """Processes ESI actions from the queue asynchronously.

    Args:
        name (str): Worker name for logging.
        queue (asyncio.Queue): Queue containing EsiAction objects.
        session (aiohttp.ClientSession): HTTP session for requests.
        queue_state (QueueState): Shared state object for queue statistics and error handling.

    Returns:
        None

    """
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
        etag = ""
        try:
            match action.request.method.lower():
                case "get":
                    response = await _do_get_request(
                        esi_request=action.request,
                        session=session,
                    )
                case _:
                    raise ValueError(f"Unsupported method: {action.request.method}")
            update_error_limits(response.headers, queue_state)
        except Exception as e:
            logger.error(f"{name} - Error processing request: {e} for {action!r}")
            queue_state.stop_operations = True
        finally:
            queue_state.processed += 1
            queue.task_done()


async def _do_get_request(
    esi_request: EsiRequest,
    session: aiohttp.ClientSession,
) -> EsiResponse:
    if esi_request.etag:
        headers = {"If-None-Match": esi_request.etag, **esi_request.headers}
    else:
        headers = esi_request.headers

    async with session.request(
        method=esi_request.method,
        url=esi_request.url,
        headers=headers,
        params=esi_request.query_params,
    ) as response:
        async with response:
            match response.status:
                case 200:
                    logger.debug(
                        f"{response.method} {response.real_url} returned "
                        f"{response.status} {response.reason}"
                    )
                case 304:
                    logger.debug(
                        f"{response.method} {response.real_url} returned "
                        f"{response.status} {response.reason}"
                    )
                case status_code if 400 <= status_code < 500:
                    logger.warning(
                        f"{response.method} {response.real_url} returned "
                        f"{response.status} {response.reason}"
                    )
                case status_code if 500 <= status_code < 600:
                    logger.error(
                        f"{response.method} {response.real_url} returned "
                        f"{response.status} {response.reason}"
                    )
                case _:
                    logger.error(
                        f"UNUSUAL STATUS: {response.method} {response.real_url} returned "
                        f"{response.status} {response.reason}"
                    )
            text = await response.text()
            return EsiResponse(
                status_code=response.status,
                status_reason=response.reason or "",
                headers=tuple(response.headers.items()),
                text=text,
                cache_key=esi_request.cache_key,
                real_url=str(response.real_url),
                completed_on=now_utc().isoformat(),
            )


async def _run_tasks(
    workers: int,
    worker: WorkerType,
    actions: Iterable[EsiAction],
    queue_state: QueueState,
):
    queue = asyncio.Queue()
    for action in actions:
        queue.put_nowait(action)
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(worker(f"Worker-{i}", queue, session, queue_state))
            for i in range(1, workers + 1)
        ]
        await asyncio.gather(*tasks)


def _run_action_set(
    actions: Sequence[EsiAction],
    queue_state: QueueState,
    max_concurrent_requests: int = 50,
) -> QueueState:
    """Run a set of ESI actions asynchronously with a specified number of workers.

    Args:
        actions (Sequence[EsiAction]): A sequence of EsiAction objects to be processed.
        queue_state (QueueState): Mutable state used to track queue progress; updated in-place.
        max_concurrent_requests (int, optional): The maximum number of concurrent requests. Defaults to 50.

    Returns:
        QueueState: The final state of the queue after processing all actions.
    """
    if len(actions) > max_concurrent_requests:
        workers = max_concurrent_requests
    else:
        workers = len(actions)
    queue_state.remaining = len(actions)
    asyncio.run(_run_tasks(workers, build_worker(), actions, queue_state))
    return queue_state


@dataclass
class ActionRunState:
    cachable: dict[UUID, EsiAction] = field(default_factory=dict)
    uncachable: dict[UUID, EsiAction] = field(default_factory=dict)
    cachable_paged: dict[UUID, EsiAction] = field(default_factory=dict)
    uncachable_paged: dict[UUID, EsiAction] = field(default_factory=dict)
    all_actions_map: dict[UUID, EsiAction] = field(default_factory=dict)
    finished: set[UUID] = field(default_factory=set)
    errored: set[UUID] = field(default_factory=set)
    check_304: set[UUID] = field(default_factory=set)


def _build_action_run_state(actions: Sequence[EsiAction]) -> ActionRunState:
    cachable: dict[UUID, EsiAction] = {
        x.request.request_id: x for x in actions if x.request.cache_key
    }
    uncachable: dict[UUID, EsiAction] = {
        x.request.request_id: x for x in actions if not x.request.cache_key
    }
    cachable_paged: dict[UUID, EsiAction] = {
        x.request.request_id: x
        for x in actions
        if x.request.cache_key and x.request.paged
    }
    uncachable_paged: dict[UUID, EsiAction] = {
        x.request.request_id: x
        for x in actions
        if not x.request.cache_key and x.request.paged
    }
    all_actions_map = {**cachable, **uncachable}
    return ActionRunState(
        cachable=cachable,
        uncachable=uncachable,
        cachable_paged=cachable_paged,
        uncachable_paged=uncachable_paged,
        all_actions_map=all_actions_map,
    )


def run_esi_actions(
    actions: Sequence[EsiAction],
    cache: EsiCacheProtocol | None,
    max_concurrent_requests: int = 50,
) -> QueueState:
    """Run ESI actions asynchronously with a specified number of workers.

    Args:
        actions (Sequence[EsiAction]): A sequence of EsiAction objects to be processed.
        workers (int, optional): The number of concurrent worker tasks. Defaults to 4.

    Returns:
        QueueState: The final state of the queue after processing all actions.
    """
    run_state = _build_action_run_state(actions)
    if cache:
        check_cache(run_state, cache)

    action_set = [
        x
        for key, x in run_state.all_actions_map.items()
        if key not in run_state.finished
    ]
    queue_state = QueueState()
    _run_action_set(
        actions=action_set,
        queue_state=queue_state,
        max_concurrent_requests=max_concurrent_requests,
    )
    mark_errored(run_state)
    check_304(run_state, cache)
    check_200(run_state, cache)
    complete_paged_actions(run_state, max_concurrent_requests)


def mark_errored(run_state: ActionRunState) -> None:
    for key, action in run_state.all_actions_map.items():
        if not action.response:
            run_state.errored.add(key)
        elif action.response and action.response.status_code not in (200, 304):
            run_state.errored.add(key)


def page_count(response: EsiResponse) -> int:
    """Get the page count from the response headers."""
    for header in response.headers:
        if header[0].lower() == "x-pages":
            return int(header[1] or 1)
    return 1


# TODO gather header functions in one place
def last_modified(response: EsiResponse) -> str | None:
    """Get the last modified timestamp from the response headers."""
    for header in response.headers:
        if header[0].lower() == "last-modified":
            return header[1]
    return None


def build_paged_actions(action: EsiAction) -> list[EsiAction]:
    """Build a list of paged actions from a single action."""
    if action.response is None:
        return []
    paged_actions = []
    pages = page_count(action.response)
    for page in range(2, pages + 1):
        request = deepcopy(action.request)
        request.query_params = {**request.query_params, "page": page}
        request.parent_id = action.request.request_id
        request.parent_last_modified = last_modified(action.response)
        paged_action = EsiAction(
            request=request,
            response=None,
        )
        paged_actions.append(paged_action)

    if action.request.paged:
        paged_actions.append(action)
    return paged_actions


def _check_last_modified(paged_action: EsiAction) -> bool:
    if not paged_action.response:
        return False
    if (
        last_modified(paged_action.response)
        != paged_action.request.parent_last_modified
    ):
        logger.error(
            f"Paged response data changed for parent request {paged_action.request.parent_id}"
            f" url: {paged_action.response.real_url}"
        )
        return False
    return True


def _collect_paged_responses(
    parent_action: EsiAction, paged_actions: Sequence[EsiAction]
) -> list[str]:
    """Collect the text content from all paged responses."""
    responses = []
    for paged_action in paged_actions:
        if paged_action.response and paged_action.response.status_code == 200:
            responses.append(paged_action.response.text)
        else:
            logger.error(
                f"Failed to collect paged response for parent request {parent_action.request.request_id}"
                f" url: {paged_action.response.real_url if paged_action.response else 'N/A'}"
            )
            raise ValueError("Incomplete paged responses")
    return responses


def complete_paged_actions(run_state: ActionRunState, max_concurrent_requests: int):
    for key, action in run_state.all_actions_map.items():
        if not action.response:
            run_state.errored.add(key)
            continue
        if action.request.paged and key not in run_state.finished:
            paged_actions = build_paged_actions(action)
            queue_state = QueueState()
            _run_action_set(
                actions=paged_actions,
                queue_state=queue_state,
                max_concurrent_requests=max_concurrent_requests,
            )
            try:
                responses = _collect_paged_responses(action, paged_actions)
                action.response.paged_responses = responses
                run_state.finished.add(key)
            except ValueError:
                run_state.errored.add(key)
                continue


def check_200(run_state: ActionRunState, cache: EsiCacheProtocol | None) -> None:
    """Check for 200 OK responses and update cache if necessary."""
    for key, action in run_state.all_actions_map.items():
        if action.response and action.response.status_code == 200:
            if cache and action.request.cache_key and not action.request.paged:
                metadata = cache.build_metadata(action.response)
                cache.set(action.request.cache_key, metadata, action.response)
            run_state.finished.add(key)


def check_304(run_state: ActionRunState, cache: EsiCacheProtocol | None) -> None:
    """Check for 304 Not Modified responses and update cache if necessary."""
    if not run_state.check_304:
        return
    if not cache:
        raise ValueError("Cache is required to process 304 responses.")
    values = list(run_state.check_304)
    for key in values:
        action = run_state.cachable[key]
        if action.request.cache_key:
            if action.response and action.response.status_code == 304:
                cache.update_304(action.request.cache_key, action.response)
                action.response = cache.get_response(action.request.cache_key)
                run_state.finished.add(key)


def check_cache(run_state: ActionRunState, cache: EsiCacheProtocol) -> None:
    for key, action in run_state.cachable.items():
        if not action.request.cache_key:
            continue
        match cache.status(action.request.cache_key):
            case CacheStatus.HIT:
                action.response = cache.get_response(action.request.cache_key)
                run_state.finished.add(key)
            case CacheStatus.MISS:
                pass
            case CacheStatus.STALE:
                metadata = cache.get_cache_metadata(action.request.cache_key)
                action.request.etag = metadata.etag
                run_state.check_304.add(key)
    return
