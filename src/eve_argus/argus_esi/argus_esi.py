"""Top level api to get data from ESI using an Argus ESI client."""

import logging

from eve_argus.argus_esi import argus_esi_actions as EAA
from eve_argus.argus_esi import esi_to_argus as DI
from eve_argus.esi_client.esi_client_protocol import EsiClientProtocol
from eve_argus.models import argus as EAM

logger = logging.getLogger(__name__)


class ArgusEsi:
    def __init__(self, esi_client: EsiClientProtocol):
        """Initialize the Argus Esi client."""
        self.esi_client = esi_client

    def market_history(self, region_id: int, type_id: int) -> EAM.MarketHistory:
        """Get market history for a specific region and type."""
        action = EAA.market_history(region_id, type_id)
        self.esi_client.get_esi_data(action)
        if action.response is None:
            raise ValueError("No response received for market history request.")
        result = DI.market_history(
            region_id=region_id,
            type_id=type_id,
            data=action.response.data,
        )
        return result
