"""Top level api to get data from ESI using an Argus ESI client."""

import logging

from eve_argus.argus_esi import esi_to_argus as DI
from eve_argus.argus_esi import request_builder as RB
from eve_argus.eve_argus_esi.esi_client.esi_client_protocol import EsiClientProtocol
from eve_argus.eve_argus_esi.esi_models import EsiAction
from eve_argus.models import argus as EAM

logger = logging.getLogger(__name__)


class ArgusEsi:
    def __init__(self, esi_client: EsiClientProtocol):
        """Initialize the Argus Esi client."""
        self.esi_client = esi_client

    def market_history(self, region_id: int, type_id: int) -> EAM.MarketHistory:
        """Get market history for a specific region and type."""
        action = EsiAction(request=RB.market_history(region_id, type_id))
        self.esi_client.get_op(action, cache_results=True, override_cached=False)
        return DI.market_history(action)
