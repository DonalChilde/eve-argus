"""Helper function for getting cache field info from ESI responses."""

from typing import TypedDict

from eve_argus.models.esi import EsiResponse


class CacheFields(TypedDict):
    """TypedDict for cache fields in ESI responses."""

    etag: str | None
    """The ETag header value."""
    last_modified: str | None
    """The Last-Modified header value."""
    expires: str | None
    """The Expires header value."""


def get_cache_fields(response: EsiResponse | None) -> CacheFields:
    """Get the cache fields from the ESI response."""
    if response is None or response.headers is None:
        return CacheFields(etag=None, last_modified=None, expires=None)
    return CacheFields(
        etag=response.headers.get("ETag"),
        last_modified=response.headers.get("Last-Modified"),
        expires=response.headers.get("Expires"),
    )
