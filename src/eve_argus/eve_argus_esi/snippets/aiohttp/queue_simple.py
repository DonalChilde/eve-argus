"""A snippet for queued aiohttp requests.

This snippet should do one or more queued aiohttp requests.
Basic rate limits can be achieved by controlling the number of concurrent requests.
The AiohttpAction objects are used to pass the results of the requests back to the caller.
Workers can signal a failure such that all remaining tasks are skipped in the next task loop.
Skipped actions result in:
    AiohttpResponse = None
    AiohttpRequestStatus.current_state = RequestState.SKIPPED
"""

import asyncio
import logging
from asyncio import Queue
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from time import perf_counter
from typing import Any, Literal
from uuid import UUID, uuid4

import aiohttp

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# TODO refactor this so that the worker function can be easily customized.


@dataclass(slots=True)
class AiohttpRequest:
    """Aiohttp request data class."""

    method: Literal["GET", "POST", "PUT", "DELETE"]
    url: str
    query_params: dict[str, str | int | float] = field(default_factory=dict)
    headers: list[tuple[str, str]] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)
    """Any additional commands to pass to Aiohttp.ClientSession.request."""
    request_id: UUID = field(default_factory=uuid4)
    parent_id: UUID | None = None
    external_id: UUID | None = None
    """A UUID used to match an AiohttpRequest with an external request."""


@dataclass(slots=True)
class AiohttpResponse:
    status_code: int
    status_reason: str | None
    headers: Sequence[tuple[str, str]]
    text: str
    """The response body as a string."""
    response_completed: str
    """The datetime the response completed, in UTC, in ISO Format."""

    uuid: UUID = field(default_factory=uuid4)
    request_id: UUID | None = None


class RequestState(StrEnum):
    """Request status codes for aiohttp requests."""

    NEW = "NEW"
    WORKING = "WORKING"
    FINISHED = "FINISHED"
    SKIPPED = "SKIPPED"


@dataclass(slots=True)
class AiohttpRequestStatus:
    request_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    current_state: RequestState = RequestState.NEW


@dataclass(slots=True)
class AiohttpAction:
    request: AiohttpRequest
    request_status: AiohttpRequestStatus
    response: AiohttpResponse | None = None


class Signals(StrEnum):
    WORKER_SHUTDOWN = "worker_shutdown"
    NORMAL_OPERATIONS = "normal_operations"


class SimpleAiohttpActionRunner:
    def __init__(self, max_concurrent_requests: int = 50) -> None:
        self.runner_status: Signals = Signals.NORMAL_OPERATIONS
        self.max_concurrent_requests = max_concurrent_requests

    async def _make_request(
        self,
        name: str,
        aiohttp_action: AiohttpAction,
        session: aiohttp.ClientSession,
    ) -> None:
        task_start = perf_counter()
        aiohttp_action.request_status.current_state = RequestState.WORKING
        logger.info(
            f"Worker {name} processing action: {aiohttp_action.request.request_id} "
            f"url: {aiohttp_action.request.url}"
        )
        async with session.request(
            aiohttp_action.request.method,
            aiohttp_action.request.url,
            params=aiohttp_action.request.query_params,
            headers=aiohttp_action.request.headers,
            **aiohttp_action.request.kwargs,
        ) as response:
            async with response:
                try:
                    aiohttp_action.request_status.request_count += 1
                    response.raise_for_status()
                    aiohttp_action.request_status.success_count += 1
                except aiohttp.ClientError as e:
                    aiohttp_action.request_status.failure_count += 1
                    aiohttp_action.request_status.current_state = RequestState.FINISHED
                    logger.error(
                        f"Worker {name} encountered an error: {e} with {aiohttp_action!r}"
                    )
                    logger.error(f"Worker {name} Triggering shutdown signal.")
                    self.runner_status = (
                        Signals.WORKER_SHUTDOWN
                    )  # Signal to stop the workers
                    # Do not re-raise so that the queue can continue processing
                    # remaining tasks, which will be marked as skipped on next loop.
                finally:
                    aiohttp_action.response = AiohttpResponse(
                        uuid=aiohttp_action.request.request_id,
                        status_code=response.status,
                        status_reason=response.reason,
                        headers=list(response.headers.items()),
                        text=await response.text(),
                        request_id=aiohttp_action.request.request_id,
                        response_completed=datetime.now(UTC).isoformat(),
                    )
                    aiohttp_action.request_status.current_state = RequestState.FINISHED
                    logger.info(
                        f"Worker {name} got status: {response.status}  reason: "
                        f"{response.reason} for action: {aiohttp_action.request.request_id} "
                        f"in {perf_counter() - task_start:.2f} seconds."
                    )

    async def _stop_on_bad_requests_worker(
        self,
        name: str,
        queue: Queue[AiohttpAction],
        session: aiohttp.ClientSession,
    ) -> None:
        """Process aiohttp actions from the queue.

        This worker processes aiohttp actions. If raise_for_status() triggers an error
        on the response, it will be logged and all the workers will see
        Signals.WORKER_SHUTDOWN the next time they process an action. This is to prevent
        excessive bad requests when the server may have signalled a malformed request. All
        remaining tasks will be skipped.
        """
        skip_tasks = False
        while True:
            aiohttp_action = await queue.get()

            if self.runner_status is Signals.WORKER_SHUTDOWN:
                logger.info(f"Worker {name} received shutdown signal.")
                skip_tasks = True
            if skip_tasks:
                aiohttp_action.request_status.current_state = RequestState.SKIPPED
                logger.info(
                    f"Worker {name} skipping action: {aiohttp_action.request.request_id} "
                    f"url: {aiohttp_action.request.url}"
                )
            else:
                await self._make_request(name, aiohttp_action, session)
            queue.task_done()

    async def _run_tasks(
        self,
        workers: int,
        actions: Iterable[AiohttpAction],
    ) -> None:
        """Run the worker tasks with the specified number of workers and actions."""
        queue = asyncio.Queue[AiohttpAction]()
        for action in actions:
            await queue.put(action)
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i in range(workers):
                task: asyncio.Task = asyncio.create_task(
                    self._stop_on_bad_requests_worker(
                        f"AiohttpQueueSimpleWorker-{i}", queue=queue, session=session
                    )
                )
                tasks.append(task)

            await queue.join()
        for task in tasks:
            task.cancel()

    def do_actions(self, workers: int, actions: Iterable[AiohttpAction]) -> None:
        """Start processing aiohttp actions in a queue with the specified number of workers.

        Args:
            workers (int): The number of worker tasks to create.
            actions (Sequence[AiohttpAction]): The aiohttp actions to process.
        """
        if workers > self.max_concurrent_requests:
            _workers = self.max_concurrent_requests
            logger.info(f"Limiting workers from requested:{workers} to {_workers}")
        else:
            _workers = workers
        asyncio.run(self._run_tasks(_workers, actions))
