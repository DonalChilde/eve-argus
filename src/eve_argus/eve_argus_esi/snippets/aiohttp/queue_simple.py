"""A snippet for queued aiohttp requests."""

import asyncio
import logging
from asyncio import Queue
from collections.abc import Sequence
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
    method: Literal["GET", "POST", "PUT", "DELETE"]
    url: str
    query_params: dict[str, str | int | float] = field(default_factory=dict)
    headers: list[tuple[str, str]] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)
    uuid: UUID = field(default_factory=uuid4)
    parent_uuid: UUID | None = None
    external_uuid: UUID | None = None


@dataclass(slots=True)
class AiohttpResponse:
    status_code: int
    status_reason: str | None
    headers: Sequence[tuple[str, str]]
    text: str
    kwargs: dict[str, Any] = field(default_factory=dict)
    uuid: UUID = field(default_factory=uuid4)
    request_uuid: UUID | None = None


@dataclass(slots=True)
class AiohttpAction:
    request: AiohttpRequest
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
    excessive bad requests when the server may have signalled a malformed request.
    """
    while True:
        aiohttp_action = await queue.get()
        task_start = perf_counter()
        if aiohttp_action is Signals.WORKER_SHUTDOWN:
            logger.info(f"Worker {name} received shutdown signal.")
            queue.put_nowait(Signals.WORKER_SHUTDOWN)  # Signal to stop the workers
            break
        logger.info(
            f"Worker {name} processing action: {aiohttp_action.request.uuid} url: {aiohttp_action.request.url}"
        )
        async with session.request(
            aiohttp_action.request.method,
            aiohttp_action.request.url,
            params=aiohttp_action.request.query_params,
            headers=aiohttp_action.request.headers,
            **aiohttp_action.request.kwargs,
        ) as response:
            task_duration = perf_counter() - task_start
            async with response:
                logger.info(
                    f"Worker {name} got status: {response.status}  reason: {response.reason} for action: {aiohttp_action.request.uuid} in {task_duration:.2f} seconds."
                )
                try:
                    response.raise_for_status()
                except aiohttp.ClientError as e:
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
                        uuid=aiohttp_action.request.uuid,
                        status_code=response.status,
                        status_reason=response.reason,
                        headers=list(response.headers.items()),
                        text=await response.text(),
                        request_uuid=aiohttp_action.request.uuid,
                    )
            logger.info(
                f"Worker {name} finished action: {aiohttp_action.request.uuid} in {perf_counter() - task_start:.2f} seconds."
            )
        queue.task_done()


async def run_tasks(
    workers: int,
    actions: Sequence[AiohttpAction],
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


def do_actions(workers: int, actions: Sequence[AiohttpAction]) -> None:
    """Start processing aiohttp actions in a queue with the specified number of workers.

    Args:
        workers (int): The number of worker tasks to create.
        actions (Sequence[AiohttpAction]): The aiohttp actions to process.
    """
    asyncio.run(run_tasks(workers, actions))
