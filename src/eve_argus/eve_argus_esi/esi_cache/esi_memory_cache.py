"""Cache for Esi get requests."""

import logging
from copy import deepcopy

from eve_argus.eve_argus_esi.esi_models import EsiResponse

from .esi_cache_protocol import EsiCacheProtocol

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class EsiMemoryCache(EsiCacheProtocol):
    """A simple in-memory cache for ESI responses."""

    def __init__(self) -> None:
        self._cache: dict[str, EsiResponse] = {}

    def get(self, key: str) -> EsiResponse | None:
        """Retrieve a cached response by its key."""
        cached_value = self._cache.get(key)
        if cached_value:
            logger.info(f"Cache hit for key: {key}")
        return cached_value

    def set(self, key: str, value: EsiResponse) -> None:
        """Store a response in the cache with its key."""
        copied_value = deepcopy(value)
        copied_value.source = "esi_cache"
        self._cache[key] = copied_value

    def clear(self) -> None:
        """Clear the entire cache."""
        self._cache.clear()

    def remove(self, key: str) -> None:
        """Remove a cached response by its key."""
        self._cache.pop(key, None)
