"""A snippet for queued aiohttp requests."""

import asyncio
import logging
from asyncio import Queue
from collections.abc import Sequence
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any, Literal
from uuid import UUID, uuid4

import aiohttp

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclass(slots=True)
class AiohttpRequest:
    method: Literal["GET", "POST", "PUT", "DELETE"]
    url: str
    query_params: dict[str, str | int | float] = field(default_factory=dict)
    headers: list[tuple[str, str]] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)
    uuid: UUID = field(default_factory=uuid4)
    parent_uuid: UUID | None = None


@dataclass(slots=True)
class AiohttpResponse:
    status_code: int
    status_reason: str | None
    headers: Sequence[tuple[str, str]]
    text: str
    kwargs: dict[str, Any] = field(default_factory=dict)
    uuid: UUID = field(default_factory=uuid4)


@dataclass(slots=True)
class AiohttpAction:
    request: AiohttpRequest
    response: AiohttpResponse | None = None


async def worker(
    name: str, queue: Queue[AiohttpAction], session: aiohttp.ClientSession
) -> None:
    not_error_flagged = True
    while not_error_flagged:
        aiohttp_action = await queue.get()
        task_start = perf_counter()
        if aiohttp_action is None:
            logger.info(f"Worker {name} received shutdown signal.")
            break
        logger.info(f"Worker {name} processing action: {aiohttp_action.request.uuid}")
        # await self.get_session()
        # if self._session is None:
        #     raise ValueError("Aiohttp session is not initialized.")

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
                    not_error_flagged = False
                    raise e

                aiohttp_action.response = AiohttpResponse(
                    uuid=aiohttp_action.request.uuid,
                    status_code=response.status,
                    status_reason=response.reason,
                    headers=list(response.headers.items()),
                    text=await response.text(),
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
    queue = asyncio.Queue()
    for action in actions:
        await queue.put(action)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(workers):
            task: asyncio.Task = asyncio.create_task(
                worker(f"Worker-{i}", queue=queue, session=session)
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
