"""Protocol required for ESI client requests and responses."""

from collections.abc import Sequence
from typing import Protocol

from eve_argus.models.esi import EsiAction

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
