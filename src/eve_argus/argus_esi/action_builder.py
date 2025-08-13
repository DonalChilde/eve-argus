"""This module contains functions to build EsiAction objects."""

from typing import Literal

from eve_argus.esi_schema.eve_openapi import EveOpenApiProtocol
from eve_argus.models.esi import EsiAction, EsiRequest, EsiResponse


class ArgusEsiActionBuilder:
    def __init__(self, eve_open_api: EveOpenApiProtocol) -> None:
        self.eve_open_api = eve_open_api

    def get_markets_prices(self, esi_action: EsiAction) -> EsiAction:
        """Get the market prices for a given ESI action."""
        # Build the request


def build_request(
    operation_id: str, parameters: dict[str, str], eve_openapi: EveOpenApiProtocol
) -> EsiRequest:
    """Build an EsiRequest object."""
    # add a helper function to EveOpenApiProtocol that verifys and splits parameters.
    # split the parameters into path, query, and header dicts using the EveOpenApiProtocol.
    # Assemble the request
