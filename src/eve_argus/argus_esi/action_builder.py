"""This module contains functions to build EsiAction objects."""

from typing import Literal

from eve_argus.esi_client.eve_openapi import EveOpenApiProtocol
from eve_argus.models.esi import EsiAction, EsiRequest, EsiResponse


class ArgusEsiActionBuilder:
    def __init__(self, eve_open_api: EveOpenApiProtocol) -> None:
        self.eve_open_api = eve_open_api

    def get_markets_prices(self, esi_action: EsiAction) -> EsiAction:
        """Get the market prices for a given ESI action."""
        # Build the request
