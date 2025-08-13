"""Eve Argus ESI Cache Protocol."""

from typing import Protocol

from eve_argus.eve_argus_esi.esi_models import EsiResponse


class EsiCacheProtocol(Protocol):
    """Protocol for ESI cache operations."""

    def get(self, key: str) -> EsiResponse | None:
        """Get an EsiResponse from the cache."""
        ...

    def set(self, key: str, value: EsiResponse) -> None:
        """Set an EsiResponse in the cache."""
        ...

    def remove(self, key: str) -> None:
        """Remove an EsiResponse from the cache."""
        ...

    def clear(self) -> None:
        """Clear the cache."""
        ...
