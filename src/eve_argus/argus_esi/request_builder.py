"""This module contains functions to build EsiAction objects."""

from uuid import uuid4

from eve_argus.eve_argus_esi.esi_models import EsiRequest


# TODO function to get cache_key from EsiRequest
def market_history(region_id: int, type_id: int) -> EsiRequest:
    """Get the market history for a specific item in a specific region."""
    request = EsiRequest(
        request_id=uuid4(),
        op_id="GetMarketsRegionIdHistory",
        method="GET",
        path_params={"region_id": region_id},
        query_params={"type_id": type_id},
    )
    return request


def market_prices() -> EsiRequest:
    """Get the adjusted and average prices for all items in the market."""
    request = EsiRequest(
        request_id=uuid4(),
        op_id="GetMarketsPrices",
        method="GET",
        path_params={},
    )
    return request


def market_orders(region_id: int) -> EsiRequest:
    """Get the current market orders for a specific region."""
    request = EsiRequest(
        request_id=uuid4(),
        op_id="GetMarketsRegionIdOrders",
        method="GET",
        path_params={"region_id": region_id},
        query_params={"order_type": "all"},
    )
    return request
