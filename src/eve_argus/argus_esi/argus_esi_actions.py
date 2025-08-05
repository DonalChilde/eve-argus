"""Action builders for ESI requests."""

from uuid import uuid4

from eve_argus.models.esi import EsiAction, EsiRequest


def market_history(region_id: int, type_id: int) -> EsiAction:
    """Build an ESI action for market history."""
    esi_request = EsiRequest(
        request_id=uuid4(),
        op_id="get_markets_region_id_history",
        arguments={"region_id": str(region_id), "type_id": str(type_id)},
    )
    return EsiAction(request=esi_request)


def universe_market_prices() -> EsiAction:
    """Build an ESI action for universe market prices."""
    esi_request = EsiRequest(
        request_id=uuid4(),
        op_id="get_markets_prices",
    )
    return EsiAction(request=esi_request)


def active_market_orders_types(region_id: int) -> EsiAction:
    """Build an ESI action for type_ids with active market orders in a region."""
    esi_request = EsiRequest(
        request_id=uuid4(),
        op_id="get_markets_region_id_orders",
        arguments={"region_id": str(region_id)},
    )
    return EsiAction(request=esi_request)


def market_orders_by_region(region_id: int) -> EsiAction:
    """Build an ESI action for market orders by region."""
    esi_request = EsiRequest(
        request_id=uuid4(),
        op_id="get_markets_region_id_orders",
        arguments={"region_id": str(region_id)},
    )
    return EsiAction(request=esi_request)


def system_cost_indices() -> EsiAction:
    """Build an ESI action for system cost indices."""
    esi_request = EsiRequest(
        request_id=uuid4(),
        op_id="get_industry_systems",
    )
    return EsiAction(request=esi_request)
