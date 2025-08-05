"""Protocol required for ESI client requests and responses."""

from collections.abc import Sequence
from typing import Protocol

from eve_argus.models.esi import EsiAction

# Esi Client knows about paging, automatically handles it.


class EsiClientProtocol(Protocol):
    """Protocol for ESI client operations."""

    def get_esi_data(
        self,
        action: EsiAction,
    ) -> None:
        """Perform a get operation against eve ESI."""
        ...

    def get_esi_data_batch(self, actions: Sequence[EsiAction]) -> None:
        """Perform multiple get operations against eve ESI."""
        ...
