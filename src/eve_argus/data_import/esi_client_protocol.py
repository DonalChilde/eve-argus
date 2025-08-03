"""Protocol required for ESI client requests and responses."""

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from eve_argus.models.esi import EsiAction, EsiRequest


class EsiClientProtocol(Protocol):
    """Protocol for ESI client operations."""

    def get_esi_data(
        self,
        request: EsiRequest,
    ) -> EsiAction:
        """Get operation data from ESI."""
        ...

    def get_paged_esi_data(
        self,
        request: EsiRequest,
    ) -> Sequence[EsiAction]:
        """Get paged operation data from ESI."""
        ...
