import asyncio
import logging
import random
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
class AiohttpAction:
    method: Literal["GET", "POST", "PUT", "DELETE"]
    url: str
    params: dict[str, str | int | float | None] = field(default_factory=dict)
    headers: dict[str, str | None] = field(default_factory=dict)
    callbacks: list[Callable[[aiohttp.ClientResponse, Queue], None]] = field(
        default_factory=list
    )
    kwargs: dict[str, Any] = field(default_factory=dict)
    uuid: UUID = field(default_factory=uuid4)


class AiohttpQueueSimple:
    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        queue: asyncio.Queue | None = None,
        worker_factory: Callable[[str, Queue], Awaitable[None]] | None = None,
    ) -> None:
        self._queue = queue or asyncio.Queue()
        self._session = session or aiohttp.ClientSession()
        self._worker_factory: Callable[[str, Queue], Awaitable[None]] = (
            worker_factory or self._worker
        )
        self._worker_count = 0

    async def _worker(self, name: str, queue: Queue) -> None:
        while True:
            aiohttp_action = await queue.get()
            task_start = perf_counter()
            if aiohttp_action is None:
                # If there are no tasks in queue, sleep for a random short time waiting for a new task.
                # This is to keep workers alive so that tasks can be added to the queue in real time.
                # The random factor is to keep all the workers from making calls at the same time.
                await asyncio.sleep(random.uniform(0.5, 1.0))
                continue
            logger.info(f"Worker {name} processing action: {aiohttp_action.uuid}")
            async with self._session as session:
                async with session.request(
                    aiohttp_action.method,
                    aiohttp_action.url,
                    params=aiohttp_action.params,
                    headers=aiohttp_action.headers,
                    **aiohttp_action.kwargs,
                ) as response:
                    task_duration = perf_counter() - task_start
                    logger.info(
                        f"Worker {name} got status response {response.status} to action: {aiohttp_action.uuid} in {task_duration:.2f} seconds."
                    )
                    for callback in aiohttp_action.callbacks:
                        callback(response, queue)
                    logger.info(
                        f"Worker {name} finished {len(aiohttp_action.callbacks)} callbacks for action: {aiohttp_action.uuid} in {perf_counter() - task_start:.2f} seconds."
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
        asyncio.run(self._run_tasks(workers, actions))
