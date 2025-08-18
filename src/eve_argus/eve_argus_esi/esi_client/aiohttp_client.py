"""Aiohttp-based implementation of the ESI client protocol."""

import logging
from collections.abc import Sequence
from copy import deepcopy
from datetime import UTC, datetime
from uuid import UUID, uuid4

from eve_argus.eve_argus_esi.esi_cache.esi_cache_protocol import (
    CacheStatus,
    EsiCacheProtocol,
)
from eve_argus.eve_argus_esi.esi_models import (
    CacheMetadataSource,
    EsiAction,
    EsiCacheMetadata,
    EsiResponse,
    ResponseDataSource,
)
from eve_argus.eve_argus_esi.helpers.esi_datetime import parse_esi_datetime
from eve_argus.eve_argus_esi.snippets.aiohttp.queue_simple import (
    AiohttpAction,
    AiohttpRequest,
    AiohttpRequestStatus,
    AiohttpResponse,
    SimpleAiohttpActionRunner,
)
from eve_argus.helpers.cache_id_from_url import cache_id_from_url
from eve_argus.helpers.esi_cache_url import compile_cache_url

from ..esi_schema.eve_openapi import EveOpenApi
from .esi_client_protocol import EsiClientProtocol

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def cache_expired_or_missing(cached_metadata: EsiCacheMetadata | None) -> bool:
    """Check if the cached result is expired or missing."""
    if cached_metadata is None:
        return True
    if datetime.fromisoformat(cached_metadata.expires) < datetime.now(UTC):
        return True
    return False


class ArgusAiohttpClient(EsiClientProtocol):
    """Aiohttp-based implementation of the ESI client protocol."""

    USER_AGENT: str = "Eve Argus (pfmsoft.dev@gmail.com; +https://github.com/DonalChilde/eve-argus; eve:Donal Childe)"

    def __init__(
        self,
        cache: EsiCacheProtocol,
        api_spec: EveOpenApi,
        base_url: str,
        user_agent_prefix: str,
        max_connections: int = 50,
        request_divisor: int = 5,
    ) -> None:
        self.cache = cache
        self.api_spec = api_spec
        self.base_url = base_url
        self.max_connections = max_connections
        self.request_divisor = request_divisor
        self.user_agent_prefix = user_agent_prefix

    def _compile_cache_key(self, esi_action: EsiAction) -> UUID:
        """Compile the cache key for a given ESI action."""
        cache_url = compile_cache_url(
            base_url=self.base_url,
            request=esi_action.request,
            open_api=self.api_spec,
        )
        return cache_id_from_url(cache_url)

    # def _inject_user_agent(self, aiohttp_action: AiohttpAction) -> None:
    #     """Inject the User-Agent header into the aiohttp action."""
    #     aiohttp_action.request.headers.append(
    #         ("User-Agent", f"{self.user_agent_prefix} -> {self.USER_AGENT}")
    #     )

    def _do_actions(
        self,
        esi_actions: dict[UUID, EsiAction],
        override_cached: bool = False,
    ) -> dict[UUID, AiohttpAction]:
        """Convert ESI actions to Aiohttp actions, and perform those actions.

        Returns a dict of Aiohttp actions, indexed by EsiAction.EsiRequest.request_id.
        If an http error >= 400 occurs, the AiohttpAction may have response=None
        for skipped actions, or a response with status etc for failed actions.
        """
        aiohttp_actions: dict[UUID, AiohttpAction] = {}
        for esi_action in esi_actions.values():
            aiohttp_action = self._build_aiohttp_action(esi_action, override_cached)
            if aiohttp_action.request.external_id is None:
                raise ValueError("Aiohttp action external_id is None.")
            # The external_id is the EsiAction.EsiRequest.request_id
            aiohttp_actions[aiohttp_action.request.external_id] = aiohttp_action
        max_workers = self._calculate_max_workers(len(aiohttp_actions))
        action_runner = SimpleAiohttpActionRunner()
        action_runner.do_actions(max_workers, aiohttp_actions.values())
        return aiohttp_actions

    def _calculate_max_workers(self, tasks: int) -> int:
        return min(self.max_connections, max(1, tasks // self.request_divisor))

    def _do_paged_actions(self, paged_actions: Sequence[AiohttpAction]) -> None:
        """Perform the paged actions."""
        if not paged_actions:
            return
        worker_count = self._calculate_max_workers(len(paged_actions))
        action_runner = SimpleAiohttpActionRunner()
        action_runner.do_actions(worker_count, paged_actions)

    def _build_paged_actions(
        self, aiohttp_action: AiohttpAction
    ) -> list[AiohttpAction]:
        """Build a list of page requests from the parent AiohttpAction.response."""
        page_count = self.check_for_pages(aiohttp_action)
        paged_actions = []
        if page_count > 1:
            for page in range(2, page_count + 1):
                page_request_action = deepcopy(aiohttp_action)
                page_request_action.request.query_params["page"] = page
                page_request_action.request_status = AiohttpRequestStatus()
                page_request_action.request.request_id = uuid4()
                paged_actions.append(page_request_action)
        return paged_actions

    def _build_aiohttp_action(
        self,
        action: EsiAction,
        override_cached: bool = False,
    ) -> AiohttpAction:
        """Build an AiohttpAction from an EsiAction."""
        url = self.api_spec.get_url(
            base_url=self.base_url,
            op_id=action.request.op_id,
            path_params=action.request.path_params,
            query_params=action.request.query_params,
        )
        headers = {
            **action.request.headers,
            "User-Agent": f"{self.user_agent_prefix} -> {self.USER_AGENT}",
        }
        if action.cache_metadata and not override_cached:
            headers["If-None-Match"] = action.cache_metadata.etag
        return AiohttpAction(
            AiohttpRequest(
                method=action.request.method,
                url=url,
                headers=[
                    (key, value) for key, value in headers.items() if value is not None
                ],
                query_params=action.request.query_params,
                external_id=action.request.request_id,  # Use the action's request_id UUID as external_id
            ),
            request_status=AiohttpRequestStatus(),
        )

    def get_operations(
        self,
        actions: dict[UUID, EsiAction],
        cache_results: bool = True,
        override_cached: bool = False,
    ) -> None:
        """Perform multiple get operations against eve ESI."""
        check_esi_cache: list[UUID] = []
        check_api: list[UUID] = []
        if not override_cached:
            check_esi_cache = self.resolve_external_metadata_expiration(
                actions, list(actions.keys())
            )
            check_api = self.resolve_for_cache(actions, check_esi_cache)
            non_success = self.resolve_for_api(actions, check_api)
        else:
            check_api = list(actions.keys())
            non_success = self.resolve_for_api(
                actions, check_api, cache_results=cache_results
            )
        if non_success:
            logger.error(
                f"{len(non_success)} Non-successful requests found: {non_success!r}"
            )
            raise ValueError(
                f"{len(non_success)} Non-successful requests: {non_success!r}"
            )

    def resolve_external_metadata_expiration(
        self, actions: dict[UUID, EsiAction], subset: Sequence[UUID]
    ) -> list[UUID]:
        unresolved_keys = []
        for key in subset:
            if actions[key].metadata_source is CacheMetadataSource.EXTERNAL:
                if cache_expired_or_missing(actions[key].cache_metadata):
                    # external cache metadata is not provided, or is expired
                    unresolved_keys.append(key)
                    continue
                else:
                    # external cache metadata is not expired
                    actions[key].response_source = ResponseDataSource.EXTERNAL
                    continue
        # No external cache metadata provided, so we need to check the API.
        unresolved_keys.append(key)
        return unresolved_keys

    def resolve_for_cache(
        self, actions: dict[UUID, EsiAction], subset: Sequence[UUID]
    ) -> list[UUID]:
        """Check the esi client cache for valid data."""
        unresolved_keys = []
        for key in subset:
            esi_action = actions[key]
            cache_key = self._compile_cache_key(esi_action)
            cache_status = self.cache.status(cache_key)
            if cache_status == CacheStatus.HIT:
                esi_action.response = self.cache.get_response(cache_key)
                esi_action.response_source = ResponseDataSource.CACHE
                esi_action.cache_metadata = self.cache.get_cache_metadata(cache_key)
                esi_action.metadata_source = CacheMetadataSource.CACHE
            else:
                unresolved_keys.append(key)
        return unresolved_keys

    def resolve_for_api(
        self,
        esi_actions: dict[UUID, EsiAction],
        subset: Sequence[UUID],
        cache_results: bool = True,
        override_cached: bool = False,
    ) -> list[UUID]:
        """Check the API for valid data.

        returns a list of keys for non-200 responses to requests.
        """
        non_success_keys = []
        api_actions = {x: esi_actions[x] for x in subset}
        aiohttp_actions = self._do_actions(api_actions)
        for key in subset:
            aiohttp_action = aiohttp_actions[key]
            esi_action = esi_actions[key]
            if aiohttp_action.response is None:
                # this signals that the action was skipped, likely a 400+ status code.
                # TODO refine the handling here.
                raise ValueError(
                    f"Aiohttp action response is None for key {key}, cannot process response."
                )
            if aiohttp_action.response.status_code == 304:
                self.handle_304(esi_action, aiohttp_action)
            elif aiohttp_action.response.status_code == 200:
                self.handle_200(esi_action, aiohttp_action, cache_results)
            else:
                non_success_keys.append(key)
        return non_success_keys

    def handle_304(
        self,
        esi_action: EsiAction,
        aiohttp_action: AiohttpAction,
        cache_results: bool = True,
    ) -> None:
        if (
            aiohttp_action.response is None
            or aiohttp_action.response.status_code != 304
        ):
            raise ValueError(
                "Aiohttp action response is None or not 304, wrong handler!"
            )

        if esi_action.metadata_source is CacheMetadataSource.EXTERNAL:
            # There was an etag match from an external source.
            esi_action.response_source = ResponseDataSource.EXTERNAL
            esi_action.cache_metadata = self.get_cache_metadata(
                aiohttp_action, cache_key=self._compile_cache_key(esi_action)
            )
            esi_action.metadata_source = CacheMetadataSource.API

        elif esi_action.metadata_source is CacheMetadataSource.CACHE:
            # There was an etag match from the esi client cache
            cache_key = self._compile_cache_key(esi_action)
            new_cache_metadata = self.get_cache_metadata(aiohttp_action, cache_key)
            response = self.cache.get_response(cache_key)
            self.cache.set(new_cache_metadata, response)
            esi_action.response_source = ResponseDataSource.CACHE
            esi_action.cache_metadata = new_cache_metadata
            esi_action.response = response
            esi_action.metadata_source = CacheMetadataSource.API
        else:
            logger.error("Metadata source missing from %r", esi_action)
            raise ValueError("Could not figure out cache metadata source.")

    def get_cache_metadata(
        self, aiohttp_action: AiohttpAction, cache_key: UUID
    ) -> EsiCacheMetadata:
        """Get the cache metadata for a given aiohttp action."""
        if aiohttp_action.response is None:
            raise ValueError(
                "Aiohttp action response is None, cannot get cache metadata."
            )
        headers = {key: value for key, value in aiohttp_action.response.headers}
        expires = headers.get("Expires", "")
        expires = parse_esi_datetime(expires).isoformat()
        etag = headers.get("ETag", "")
        last_modified = headers.get("Last-Modified", "")
        last_modified = parse_esi_datetime(last_modified).isoformat()
        return EsiCacheMetadata(
            key=cache_key,
            expires=expires,
            etag=etag,
            last_modified=last_modified,
            last_checked=aiohttp_action.response.response_completed,
        )

    def handle_200(
        self,
        esi_action: EsiAction,
        aiohttp_action: AiohttpAction,
        cache_results: bool = True,
    ) -> None:
        if (
            aiohttp_action.response is None
            or aiohttp_action.response.status_code != 200
        ):
            raise ValueError(
                "Aiohttp action response is None or not 200, wrong handler!"
            )
        cache_key = self._compile_cache_key(esi_action)
        cache_metadata = self.get_cache_metadata(aiohttp_action, cache_key)
        response = EsiResponse(
            request_url=aiohttp_action.request.url,
            cache_key=cache_key,
            text=[aiohttp_action.response.text],
        )
        esi_action.response = response
        esi_action.response_source = ResponseDataSource.API
        esi_action.cache_metadata = cache_metadata
        esi_action.metadata_source = CacheMetadataSource.API
        paged_actions = self._build_paged_actions(aiohttp_action)
        if paged_actions:
            self._do_paged_actions(paged_actions)
            result_texts = self.handle_paged_responses(paged_actions)
            response.text.extend(result_texts)
        if cache_results:
            self.cache.set(cache_metadata, response)

    def handle_paged_responses(self, actions: Sequence[AiohttpAction]) -> Sequence[str]:
        results: list[str] = []
        for action in actions:
            if action.response is None:
                raise ValueError("Aiohttp action response is None, cannot process.")
            if action.response.status_code != 200:
                raise ValueError("Aiohttp action response is not 200, cannot process.")
            results.append(action.response.text)
        return results

    def check_for_pages(self, aiohttp_action: AiohttpAction) -> int:
        """Check for pages in a aiohttp action."""
        if aiohttp_action.response is None:
            raise ValueError("Aiohttp action response is None, cannot check for pages.")
        for header in aiohttp_action.response.headers:
            if header[0].lower() == "x-pages":
                # If the header is present, return the total number of pages
                total_pages = int(header[1])
                return total_pages
        return 0
