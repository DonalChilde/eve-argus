from uuid import UUID

from pydantic import BaseModel

from eve_argus.eve_argus_esi.esi_client.models import (
    EsiResponse,
)


class EsiCacheMetadata(BaseModel):
    """Represents a cache metadata for ESI GET requests/responses."""

    cache_key: UUID
    """The cache key UUID, built from the get request url."""
    expires: str
    """The expiration time for the cache key."""
    etag: str
    """The ETag for the cached response."""
    last_modified: str
    """The last modified time for the cached response."""
    last_checked: str
    """The last time this ESI route was checked in ISO 8601 format."""


class CacheEntry(BaseModel):
    """Represents a cached entry."""

    metadata: EsiCacheMetadata
    response: str


class EsiCachedResponse(BaseModel):
    """Represents a cached ESI response."""

    cache_key: UUID
    metadata: EsiCacheMetadata
    response: EsiResponse


class EsiCache(BaseModel):
    data: dict[UUID, EsiCachedResponse] = {}
