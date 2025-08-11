"""Protocol required for ESI client requests and responses."""

from collections.abc import Sequence
from typing import Protocol

from eve_argus.models.esi import EsiAction, EsiResponse

# Esi Client knows about paging, automatically handles it.


class EsiClientProtocol(Protocol):
    """Protocol for ESI client operations."""

    def get_op(
        self,
        action: EsiAction,
        cache_result: bool = True,
        override_cached: bool = False,
    ) -> EsiAction:
        """Perform a get operation against eve ESI."""
        ...

    def get_ops(
        self,
        actions: Sequence[EsiAction],
        cache_result: bool = True,
        override_cached: bool = False,
    ) -> Sequence[EsiAction]:
        """Perform multiple get operations against eve ESI."""
        ...


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
