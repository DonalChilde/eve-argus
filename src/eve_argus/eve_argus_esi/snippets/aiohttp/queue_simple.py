"""A snippet for queued aiohttp requests."""

import asyncio
import logging
from asyncio import Queue
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
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
    request_id: UUID = field(default_factory=uuid4)
    parent_id: UUID | None = None
    external_id: UUID | None = None


@dataclass(slots=True)
class AiohttpResponse:
    status_code: int
    status_reason: str | None
    headers: Sequence[tuple[str, str]]
    text: str
    kwargs: dict[str, Any] = field(default_factory=dict)
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


async def stop_on_bad_requests_worker(
    name: str, queue: Queue[AiohttpAction | Signals], session: aiohttp.ClientSession
) -> None:
    """Process aiohttp actions from the queue.

    This worker processes aiohttp actions. If raise_for_status() triggers an error
    on the response, it will be logged and all the workers will receive
    Signals.WORKER_SHUTDOWN the next time they process an action. This is to prevent
    excessive bad requests when the server may have signalled a malformed request. All
    remaining tasks will be skipped.
    """
    skip_tasks = False
    while True:
        aiohttp_action = await queue.get()
        task_start = perf_counter()

        if aiohttp_action is Signals.WORKER_SHUTDOWN:
            logger.info(f"Worker {name} received shutdown signal.")
            queue.put_nowait(Signals.WORKER_SHUTDOWN)  # Signal to stop the workers
            skip_tasks = True
        elif skip_tasks:
            aiohttp_action.request_status.current_state = RequestState.SKIPPED
            logger.info(
                f"Worker {name} skipping action: {aiohttp_action.request.request_id} "
                f"url: {aiohttp_action.request.url}"
            )
        else:
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
                        aiohttp_action.request_status.current_state = (
                            RequestState.FINISHED
                        )
                        logger.error(
                            f"Worker {name} encountered an error: {e} with {aiohttp_action!r}"
                        )
                        logger.error(f"Worker {name} Triggering shutdown signal.")
                        queue.put_nowait(
                            Signals.WORKER_SHUTDOWN
                        )  # Signal to stop the workers
                        raise e
                    finally:
                        aiohttp_action.response = AiohttpResponse(
                            uuid=aiohttp_action.request.request_id,
                            status_code=response.status,
                            status_reason=response.reason,
                            headers=list(response.headers.items()),
                            text=await response.text(),
                            request_id=aiohttp_action.request.request_id,
                        )

                        logger.info(
                            f"Worker {name} got status: {response.status}  reason: {response.reason} for action: {aiohttp_action.request.request_id} in {task_duration:.2f} seconds."
                        )
                        task_duration = perf_counter() - task_start
                logger.info(
                    f"Worker {name} finished action: {aiohttp_action.request.request_id} in {perf_counter() - task_start:.2f} seconds."
                )
        queue.task_done()


async def run_tasks(
    workers: int,
    actions: Iterable[AiohttpAction],
) -> None:
    """Run the worker tasks with the specified number of workers and actions."""
    queue = asyncio.Queue[AiohttpAction | Signals]()
    for action in actions:
        await queue.put(action)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(workers):
            task: asyncio.Task = asyncio.create_task(
                stop_on_bad_requests_worker(
                    f"AiohttpQueueSimpleWorker-{i}", queue=queue, session=session
                )
            )
            tasks.append(task)

        await queue.join()
    for task in tasks:
        task.cancel()


def do_actions(workers: int, actions: Iterable[AiohttpAction]) -> None:
    """Start processing aiohttp actions in a queue with the specified number of workers.

    Args:
        workers (int): The number of worker tasks to create.
        actions (Sequence[AiohttpAction]): The aiohttp actions to process.
    """
    asyncio.run(run_tasks(workers, actions))
