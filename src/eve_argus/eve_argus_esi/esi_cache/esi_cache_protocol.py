"""Eve Argus ESI Cache Protocol."""

from enum import StrEnum
from typing import Protocol
from uuid import UUID

from .models import (
    EsiCachedResponse,
    EsiCacheMetadata,
    EsiResponse,
)


class CacheStatus(StrEnum):
    """Represents the cache status of an ESI response."""

    HIT = "hit"
    """A current response is available in the cache."""
    MISS = "miss"
    """The response was not found in cache."""
    STALE = "stale"
    """The cached response is stale and needs to be refreshed."""


class EsiCacheProtocol(Protocol):
    """Protocol for ESI cache operations."""

    def get(self, key: UUID) -> EsiCachedResponse | None:
        """Get an EsiResponse from the cache."""
        ...

    def get_response(self, key: UUID) -> EsiResponse:
        """Get an EsiResponse from the cache by key."""
        ...

    def get_cache_metadata(self, key: UUID) -> EsiCacheMetadata:
        """Get the cache key for an EsiResponse from the cache."""
        ...

    def update_304(self, cache_key: UUID, response: EsiResponse) -> None:
        """Update the cache metadata for a 304 response."""
        ...

    def set(
        self, cache_key: UUID, cache_metadata: EsiCacheMetadata, value: EsiResponse
    ) -> None:
        """Set an EsiResponse in the cache."""
        ...

    def remove(self, key: UUID) -> None:
        """Remove an EsiResponse from the cache."""
        ...

    def clear(self) -> None:
        """Clear the cache."""
        ...

    def status(self, cache_key: UUID) -> CacheStatus:
        """Get the cache status of an EsiResponse."""
        ...

    def build_metadata(self, response: EsiResponse) -> EsiCacheMetadata:
        """Build cache metadata for an EsiResponse."""
        ...
