"""This module contains functions to build EsiAction objects."""

from typing import Sequence
from uuid import uuid4

from eve_argus.eve_argus_esi.esi_models import EsiRequest


# TODO function to get cache_key from EsiRequest - cant remeber why i wanted this.
#   think about cache lifecycle?
def _inject_etag(request: EsiRequest, etag: str) -> None:
    """Inject the ETag into the action."""
    if etag:
        request.headers["If-None-Match"] = etag


def market_history_batch(
    region_id: int, type_ids: Sequence[int]
) -> Sequence[EsiRequest]:
    """Get the market history for multiple items in a specific region."""
    requests = []
    for type_id in type_ids:
        requests.append(market_history(region_id, type_id))
    return requests


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


def market_types(region_id: int) -> EsiRequest:
    """Get the market types for a specific region."""
    request = EsiRequest(
        request_id=uuid4(),
        op_id="GetMarketsRegionIdTypes",
        method="GET",
        path_params={"region_id": region_id},
    )
    return request
