"""Cache for Esi get requests."""

import logging
from copy import deepcopy
from datetime import UTC, datetime
from uuid import UUID

from eve_argus.eve_argus_esi.esi_models import EsiCacheMetadata, EsiResponse

from .esi_cache_protocol import CacheStatus, EsiCacheProtocol

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class EsiMemoryCache(EsiCacheProtocol):
    """A simple in-memory cache for ESI responses."""

    def __init__(self) -> None:
        self._cache: dict[UUID, EsiResponse] = {}
        self._metadata: dict[UUID, EsiCacheMetadata] = {}

    def get(self, key: UUID) -> tuple[EsiCacheMetadata, EsiResponse]:
        """Retrieve a cached response by its key."""
        cached_value = self.get_response(key)
        metadata = self.get_cache_metadata(key)
        if cached_value:
            logger.info(f"Cache hit for key: {key}")
        return (metadata, cached_value)

    def get_response(self, key: UUID) -> EsiResponse:
        """Retrieve a cached response by its key."""
        cached_value = self._cache.get(key)
        if cached_value is None:
            raise KeyError(f"No cached response found for key: {key}")
        return cached_value

    def get_cache_metadata(self, key: UUID) -> EsiCacheMetadata:
        """Retrieve cache metadata for a cached response by its key."""
        metadata = self._metadata.get(key)
        if metadata is None:
            raise KeyError(f"No cache metadata found for key: {key}")
        return metadata

    def set(self, cache_metadata: EsiCacheMetadata, value: EsiResponse) -> None:
        """Store a response in the cache with its key."""
        self._cache[cache_metadata.key] = deepcopy(value)
        self._metadata[cache_metadata.key] = deepcopy(cache_metadata)

    def clear(self) -> None:
        """Clear the entire cache."""
        self._cache.clear()
        self._metadata.clear()

    def remove(self, key: UUID) -> None:
        """Remove a cached response by its key."""
        self._cache.pop(key, None)
        self._metadata.pop(key, None)

    def status(self, cache_key: UUID) -> CacheStatus:
        """Get the cache status of an EsiResponse."""
        if cache_key in self._metadata:
            metadata = self._metadata[cache_key]
            if datetime.fromisoformat(metadata.expires).astimezone(UTC) > datetime.now(
                UTC
            ):
                return CacheStatus.HIT
            return CacheStatus.STALE
        return CacheStatus.MISS
