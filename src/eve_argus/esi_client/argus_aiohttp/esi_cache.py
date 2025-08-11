"""Cache for Esi get requests."""

from eve_argus.esi_client.esi_client_protocol import EsiCacheProtocol
from eve_argus.models.esi import EsiResponse


class EsiMemoryCache(EsiCacheProtocol):
    """A simple in-memory cache for ESI responses."""

    def __init__(self) -> None:
        self._cache: dict[str, EsiResponse] = {}

    def get(self, key: str) -> EsiResponse | None:
        """Retrieve a cached response by its key."""
        return self._cache.get(key)

    def set(self, key: str, value: EsiResponse) -> None:
        """Store a response in the cache with its key."""
        self._cache[key] = value

    def clear(self) -> None:
        """Clear the entire cache."""
        self._cache.clear()

    def remove(self, key: str) -> None:
        """Remove a cached response by its key."""
        self._cache.pop(key, None)
