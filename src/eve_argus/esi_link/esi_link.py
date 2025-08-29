import asyncio
from datetime import datetime
from uuid import UUID

import aiohttp

from eve_argus.esi_link.models import EsiQuery, QueryResponse
from eve_argus.eve_argus_esi.esi_schema.eve_openapi_protocol import EveOpenApiProtocol


class EsiLink:
    def __init__(
        self, schema: EveOpenApiProtocol, max_concurrent_requests: int = 50
    ) -> None:
        self._error_timeout_ends = datetime | None
        """The time at which queries can resume."""
        self._schema = schema
        self._max_concurrent_requests = max_concurrent_requests

    async def _worker(self, queue: asyncio.Queue):
        pass
        # define a worker to process asyncio.Queue[EsiQuery] items.

    def do_query(self, query: EsiQuery) -> QueryResponse:
        return self.do_queries({query["query_id"]: query})[query["query_id"]]

    def do_queries(self, queries: dict[UUID, EsiQuery]) -> dict[UUID, QueryResponse]:
        pass
        # Use asyncio.Queue
        # do the aiohttp.requests, and return the results.
        # wrap in a class to hold error timeouts between requests
