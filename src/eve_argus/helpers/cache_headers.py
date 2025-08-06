"""Helper function for getting cache field info from ESI responses."""

from typing import TypedDict

from eve_argus.models.esi import EsiResponse


class CacheFields(TypedDict):
    """TypedDict for cache fields in ESI responses."""

    etag: str | None
    last_modified: str | None
    expires: str | None


def get_cache_fields(response: EsiResponse) -> CacheFields:
    """Get the cache fields from the ESI response."""
    return CacheFields(
        etag=response.headers.get("ETag"),
        last_modified=response.headers.get("Last-Modified"),
        expires=response.headers.get("Expires"),
    )
