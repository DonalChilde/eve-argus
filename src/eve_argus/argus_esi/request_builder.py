"""This module contains functions to build EsiAction objects."""

from uuid import uuid4

from eve_argus.eve_argus_esi.esi_models import EsiRequest


# TODO function to get cache_key from EsiRequest - cant remeber why i wanted this.
#   think about cache lifecycle?
def _inject_etag(request: EsiRequest, etag: str) -> None:
    """Inject the ETag into the action."""
    if etag:
        request.headers["If-None-Match"] = etag


def market_history(region_id: int, type_id: int, etag: str = "") -> EsiRequest:
    """Get the market history for a specific item in a specific region."""
    request = EsiRequest(
        request_id=uuid4(),
        op_id="GetMarketsRegionIdHistory",
        method="GET",
        path_params={"region_id": region_id},
        query_params={"type_id": type_id},
    )
    _inject_etag(request, etag)
    return request


def market_prices(etag: str = "") -> EsiRequest:
    """Get the adjusted and average prices for all items in the market."""
    request = EsiRequest(
        request_id=uuid4(),
        op_id="GetMarketsPrices",
        method="GET",
        path_params={},
    )
    _inject_etag(request, etag)
    return request


def market_orders(region_id: int, etag: str = "") -> EsiRequest:
    """Get the current market orders for a specific region."""
    request = EsiRequest(
        request_id=uuid4(),
        op_id="GetMarketsRegionIdOrders",
        method="GET",
        path_params={"region_id": region_id},
        query_params={"order_type": "all"},
    )
    _inject_etag(request, etag)
    return request


def system_cost_indices(etag: str = "") -> EsiRequest:
    """Get the cost indices for the eve universe."""
    request = EsiRequest(
        request_id=uuid4(),
        op_id="GetIndustrySystems",
        method="GET",
        path_params={},
        query_params={},
    )
    _inject_etag(request, etag)
    return request
