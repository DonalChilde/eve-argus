"""A snippet for queued aiohttp requests, with per request callbacks."""

import asyncio
import logging
from asyncio import Queue
from collections.abc import Awaitable, Callable, Sequence
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


class AiohttpQueueSimple:
    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        queue: asyncio.Queue[AiohttpAction] | None = None,
        worker_factory: Callable[[str, Queue], Awaitable[None]] | None = None,
    ) -> None:
        """Provides a simple interface for processing aiohttp requests in a queue.

        Args:
            session (aiohttp.ClientSession | None): The aiohttp session to use.
                If None, a new aiohttp.ClientSession will be created.
            queue (asyncio.Queue[AiohttpAction] | None): The queue to use for actions.
                If None, a new asyncio.Queue will be created.
            worker_factory (Callable[[str, Queue], Awaitable[None]] | None): The factory
                for creating worker tasks. If None, the default worker factory will be used.
        """
        self._queue = queue or asyncio.Queue[AiohttpAction]()
        self._session = session or aiohttp.ClientSession()
        self._worker_factory: Callable[[str, Queue], Awaitable[None]] = (
            worker_factory or self._worker
        )
        self._worker_count = 0

    async def _worker(self, name: str, queue: Queue[AiohttpAction]) -> None:
        while True:
            aiohttp_action = await queue.get()
            task_start = perf_counter()
            if aiohttp_action is None:
                logger.info(f"Worker {name} received shutdown signal.")
                break
            logger.info(
                f"Worker {name} processing action: {aiohttp_action.request.uuid}"
            )
            async with self._session as session:
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
                            f"Worker {name} got status: {response.status}  reason: {response.reason} to action: {aiohttp_action.request.uuid} in {task_duration:.2f} seconds."
                        )
                        try:
                            response.raise_for_status()
                        except aiohttp.ClientError as e:
                            logger.error(f"Worker {name} encountered an error: {e}")
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

    async def _run_tasks(self, workers: int, actions: Sequence[AiohttpAction]) -> None:
        tasks = []
        for i in range(workers):
            task: asyncio.Task = asyncio.create_task(
                self._worker(f"Worker-{i}", self._queue)
            )
            tasks.append(task)
        self._worker_count = len(tasks)
        await self._queue.join()
        for task in tasks:
            task.cancel()
        self._worker_count = len(tasks)

    def do_actions(self, workers: int, actions: Sequence[AiohttpAction]) -> None:
        """Start processing aiohttp actions in a queue with the specified number of workers.

        Args:
            workers (int): The number of worker tasks to create.
            actions (Sequence[AiohttpAction]): The aiohttp actions to process.
        """
        asyncio.run(self._run_tasks(workers, actions))
