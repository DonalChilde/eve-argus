```python
from __future__ import annotations
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

# Assume these are your pydantic models (names per your doc)
# from .models import EsiAction, EsiRequest, EsiResponse, CacheMetadata
# from .cache_protocol import EsiCacheProtocol

ISO = "%Y-%m-%dT%H:%M:%S.%fZ"


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).strftime(ISO)


def _is_expired(meta: CacheMetadata | None) -> bool:
    if not meta or not meta.expires:
        return True
    try:
        return datetime.fromisoformat(meta.expires.replace("Z", "+00:00")) <= datetime.now(timezone.utc)
    except Exception:
        return True


class EsiClient:
    def __init__(self, cache: EsiCacheProtocol, http):
        """
        http must expose: request(method, url, headers=None, params=None) -> (status, headers:dict, pages:list[str])
        pages is a list of page bodies (to support pagination).
        """
        self.cache = cache
        self.http = http

    # --- public API ---
    def get_op(
        self,
        action: EsiAction,
        cache_results: bool = True,
        override_cached: bool = False,
    ) -> EsiAction:
        req = action.request

        # Non-GET: just perform request, no cache_key usage
        if req.method != "GET":
            status, headers, pages = self._perform(req)
            action.response = self._build_response(req, pages, source="esi_api", cache_key=None)
            action.cache_metadata = None
            return action

        # Derive / obtain cache_key (assume deterministic from URL incl query)
        cache_key = (action.cache_metadata.cache_key if action.cache_metadata
                     else self._compute_cache_key(req))

        supplied_meta = action.cache_metadata
        cached_meta = None
        cached_resp = None

        if not override_cached:
            cached_meta = self.cache.get_metadata(str(cache_key))
            cached_resp = self.cache.get(str(cache_key)) if cached_meta else None

        has_cache = cached_meta is not None and cached_resp is not None
        has_supplied = supplied_meta is not None

        # 4. cache hit + supplied metadata
        if has_cache and has_supplied:
            if cached_meta.etag == supplied_meta.etag:
                if _is_expired(supplied_meta):
                    return self._conditional_refresh(
                        action,
                        cache_key,
                        etag=supplied_meta.etag,
                        use_cached_on_304=False,
                        supplied_metadata=supplied_meta,
                        cached_response=None,
                    )
                # not expired, external data still valid
                action.response = None
                action.cache_metadata = supplied_meta
                return action
            # etag mismatch -> treat as stale, do full fetch
            return self._full_fetch(action, cache_key)

        # 3. cache hit, no supplied metadata
        if has_cache and not has_supplied:
            if not _is_expired(cached_meta) and not override_cached:
                action.response = cached_resp
                action.cache_metadata = cached_meta
                return action
            # expired -> conditional fetch with cached etag
            return self._conditional_refresh(
                action,
                cache_key,
                etag=cached_meta.etag,
                use_cached_on_304=True,
                supplied_metadata=None,
                cached_response=cached_resp,
            )

        # 2. no cache hit, supplied metadata
        if (not has_cache) and has_supplied:
            if not _is_expired(supplied_meta):
                action.response = None
                action.cache_metadata = supplied_meta
                return action
            # expired external metadata -> conditional fetch
            return self._conditional_refresh(
                action,
                cache_key,
                etag=supplied_meta.etag,
                use_cached_on_304=False,
                supplied_metadata=supplied_meta,
                cached_response=None,
            )

        # 1. no cache, no supplied metadata -> full fetch
        return self._full_fetch(action, cache_key)

    # --- helpers ---
    def _compute_cache_key(self, req: EsiRequest) -> UUID:
        # Simplified: you likely have a stable hash; placeholder uses uuid4 (replace!)
        return uuid4()

    def _perform(self, req: EsiRequest, extra_headers: dict[str, str] | None = None):
        headers = dict(req.headers)
        if extra_headers:
            headers.update(extra_headers)
        # Expect http.request returns (status_code:int, headers:dict, pages:list[str])
        return self.http.request(
            req.method,
            req.request_url,  # assume prebuilt full URL on request
            headers=headers,
            params=req.query_params or None,
        )

    def _build_response(
        self,
        req: EsiRequest,
        pages: list[str],
        source: Literal["esi_cache", "esi_api"],
        cache_key: UUID | None,
    ) -> EsiResponse:
        return EsiResponse(
            request_id=req.request_id,
            request_url=req.request_url,
            source=source,
            cache_key=cache_key,
            text=pages,
        )

    def _build_metadata(self, headers: dict, cache_key: UUID) -> CacheMetadata:
        return CacheMetadata(
            cache_key=cache_key,
            etag=headers.get("ETag", ""),
            last_modified=headers.get("Last-Modified", ""),
            expires=headers.get("Expires", _now_iso()),
            last_requested=_now_iso(),
        )

    def _store(self, meta: CacheMetadata, resp: EsiResponse, cache_results: bool = True):
        if cache_results:
            self.cache.set(meta, resp)

    def _full_fetch(self, action: EsiAction, cache_key: UUID) -> EsiAction:
        status, headers, pages = self._perform(action.request)
        if status != 200:
            # Simplify: raise or handle errors
            raise RuntimeError(f"Unexpected status {status}")
        meta = self._build_metadata(headers, cache_key)
        resp = self._build_response(action.request, pages, "esi_api", cache_key)
        self._store(meta, resp)
        action.response = resp
        action.cache_metadata = meta
        return action

    def _conditional_refresh(
        self,
        action: EsiAction,
        cache_key: UUID,
        etag: str,
        use_cached_on_304: bool,
        supplied_metadata: CacheMetadata | None,
        cached_response: EsiResponse | None,
    ) -> EsiAction:
        status, headers, pages = self._perform(action.request, {"If-None-Match": etag})
        if status == 304:
            # Update whichever metadata object we return
            meta = supplied_metadata or self.cache.get_metadata(str(cache_key))
            if meta:
                meta.last_requested = _now_iso()
                # Refresh expiry if server sent new one
                if "Expires" in headers:
                    meta.expires = headers["Expires"]
            action.cache_metadata = meta
            if use_cached_on_304 and cached_response:
                action.response = cached_response
            else:
                # Signal caller external data still valid
                action.response = None
            return action
        if status == 200:
            meta = self._build_metadata(headers, cache_key)
            resp = self._build_response(action.request, pages, "esi_api", cache_key)
            self._store(meta, resp)
            action.response = resp
            action.cache_metadata = meta
            return action
        raise RuntimeError(f"Unexpected status {status} in conditional fetch")

```