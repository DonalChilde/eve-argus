"""Eve Argus ESI Cache Protocol."""

from enum import StrEnum
from typing import Protocol
from uuid import UUID

from eve_argus.eve_argus_esi.esi_models import EsiCacheMetadata, EsiResponse


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

    def get(self, key: UUID) -> tuple[EsiCacheMetadata, EsiResponse]:
        """Get an EsiResponse from the cache."""
        ...

    def get_response(self, key: UUID) -> EsiResponse:
        """Get an EsiResponse from the cache by key."""
        ...

    def get_cache_metadata(self, key: UUID) -> EsiCacheMetadata:
        """Get the cache key for an EsiResponse from the cache."""
        ...

    def set(self, cache_metadata: EsiCacheMetadata, value: EsiResponse) -> None:
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
