"""Aiohttp-based implementation of the ESI client protocol."""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID

from eve_argus.esi_client.esi_client_protocol import EsiCacheProtocol, EsiClientProtocol
from eve_argus.esi_client.eve_openapi import EveOpenApi
from eve_argus.helpers.cache_id_from_url import cache_id_from_url
from eve_argus.helpers.esi_cache_url import compile_cache_url
from eve_argus.helpers.esi_datetime import parse_esi_datetime
from eve_argus.models.esi import EsiAction, EsiResponse
from eve_argus.snippets.aiohttp.queue_simple import (
    AiohttpAction,
    AiohttpRequest,
    AiohttpResponse,
    do_actions,
)


def cache_expired_or_missing(cached_result: EsiResponse | None) -> bool:
    """Check if the cached result is expired or missing."""
    if cached_result is None:
        return True
    if datetime.fromisoformat(cached_result.expires) < datetime.now(UTC):
        return True
    return False


class ArgusAiohttpClient(EsiClientProtocol):
    """Aiohttp-based implementation of the ESI client protocol."""

    def __init__(
        self,
        cache: EsiCacheProtocol,
        api_spec: EveOpenApi,
        base_url: str,
        max_connections: int = 50,
        request_divisor: int = 5,
    ) -> None:
        self.cache = cache
        self.api_spec = api_spec
        self.base_url = base_url
        self.max_connections = max_connections
        self.request_divisor = request_divisor

    def _compile_cache_key(self, esi_action: EsiAction) -> UUID:
        """Compile the cache key for a given ESI action."""
        cache_url = compile_cache_url(
            base_url=self.base_url,
            request=esi_action.request,
            open_api=self.api_spec,
        )
        return cache_id_from_url(cache_url)

    def get_op(
        self,
        esi_action: EsiAction,
        cache_results: bool = True,
        override_cached: bool = False,
    ) -> EsiAction:
        """Perform a get operation against eve ESI."""
        if esi_action.request.method != "GET":
            raise ValueError("Only GET requests are supported in this function.")
        cache_key = self._compile_cache_key(esi_action)
        cached_result = self.cache.get(str(cache_key))
        etag = cached_result.etag if cached_result else ""
        if override_cached or cache_expired_or_missing(cached_result):
            aiohttp_action = self._build_aiohttp_action(esi_action, etag=etag)
            do_actions(1, (aiohttp_action,))
            if aiohttp_action.response is None:
                raise ValueError(
                    "Aiohttp action response is None, when response should be complete."
                )
            if aiohttp_action.response.status_code == 304:
                # If the response is 304, use the cached result
                esi_action.response = cached_result
            else:
                paged_actions = self._build_paged_actions(aiohttp_action)
                self._do_paged_actions(paged_actions)
                self._process_get_responses(
                    esi_action, aiohttp_action, paged_actions, cache_key=cache_key
                )
            if cache_results:
                if esi_action.response is None:
                    raise ValueError(
                        "ESI action response is None, when response should be complete."
                    )
                self.cache.set(str(cache_key), esi_action.response)
        else:
            esi_action.response = cached_result
        return esi_action

    def _calculate_max_workers(self, tasks: int) -> int:
        return min(self.max_connections, max(1, tasks // self.request_divisor))

    def _do_paged_actions(self, paged_actions: Sequence[AiohttpAction]) -> None:
        """Perform the paged actions."""
        if not paged_actions:
            return
        worker_count = self._calculate_max_workers(len(paged_actions))
        do_actions(worker_count, paged_actions)

    def _process_get_responses(
        self,
        esi_action: EsiAction,
        aiohttp_action: AiohttpAction,
        paged_actions: Sequence[AiohttpAction],
        cache_key: UUID,
    ) -> None:
        """Process the responses from the live GET requests.

        Combines the results of the initial get action, and any resulting paged actions.
        etag, last_modified, and expires are taken from the primary response.
        """
        if aiohttp_action.response is None:
            raise ValueError(
                "Aiohttp action response is None, cannot process response."
            )
        if not all([page.response for page in paged_actions]):
            raise ValueError("Not all paged actions have responses.")
        text = [
            aiohttp_action.response.text,
            *[page.response.text for page in paged_actions if page.response],
        ]
        expires = etag = last_modified = ""
        for header in aiohttp_action.response.headers:
            if header[0].lower() == "expires":
                expires = header[1]
            elif header[0].lower() == "etag":
                etag = header[1]
            elif header[0].lower() == "last-modified":
                last_modified = header[1]
        expires = parse_esi_datetime(expires).isoformat() if expires else ""
        last_modified = (
            parse_esi_datetime(last_modified).isoformat() if last_modified else ""
        )

        esi_action.response = EsiResponse(
            request_id=esi_action.request.request_id,
            request_url=aiohttp_action.request.url,
            source="api",
            cache_key=cache_key,
            text=text,
            expires=expires,
            etag=etag,
            last_modified=last_modified,
        )

    def _build_paged_actions(
        self, aiohttp_action: AiohttpAction
    ) -> list[AiohttpAction]:
        """Build a list of page requests from the network result."""
        page_count = self._check_for_pages(aiohttp_action.response)
        paged_actions = []
        if page_count > 1:
            for page in range(2, page_count + 1):
                page_request_action = AiohttpAction(
                    AiohttpRequest(
                        method=aiohttp_action.request.method,
                        url=aiohttp_action.request.url,
                        query_params={
                            **aiohttp_action.request.query_params,
                            "page": page,
                        },
                        headers=aiohttp_action.request.headers,
                        uuid=aiohttp_action.request.uuid,
                    )
                )
                paged_actions.append(page_request_action)
        return paged_actions

    def _check_for_pages(self, network_result: AiohttpResponse | None) -> int:
        """Check the network result for pagination information."""
        if network_result is None:
            raise ValueError("Network result is None, cannot check for pages.")
        if not network_result:
            return 0
        # Check for pagination headers in the response
        for header in network_result.headers:
            if header[0].lower() == "x-pages":
                # If the header is present, return the total number of pages
                total_pages = int(header[1])
                return total_pages
        return 0

    def _build_aiohttp_action(self, action: EsiAction, etag: str = "") -> AiohttpAction:
        """Build an AiohttpAction from an EsiAction."""
        url = self.api_spec.get_url(
            base_url=self.base_url,
            op_id=action.request.op_id,
            path_params=action.request.path_params,
            query_params=action.request.query_params,
        )
        headers = {
            **action.request.headers,
            "If-None-Match": etag,
        }
        return AiohttpAction(
            AiohttpRequest(
                method=action.request.method,
                url=url,
                headers=[
                    (key, value) for key, value in headers.items() if value is not None
                ],
                query_params=action.request.query_params,
            )
        )

    def get_ops(
        self,
        actions: Sequence[EsiAction],
        cache_result: bool = True,
        override_cached: bool = False,
    ) -> Sequence[EsiAction]:
        """Perform multiple get operations against eve ESI."""
        ...
