"""Transform ESI data models to Argus data models."""

from collections.abc import Sequence
from datetime import UTC, datetime
from itertools import chain
from typing import Any
from uuid import uuid4

from eve_argus.models import argus as EAM


def market_prices_universe(
    data: Sequence[dict[str, Any]],
) -> Sequence[EAM.UniverseMarketPrice]:
    """Import market prices for the universe from a sequence of dictionaries."""
    result: list[EAM.UniverseMarketPrice] = []
    for item in data:
        prices = EAM.UniverseMarketPrice(
            type_id=item["type_id"],
            adjusted_price=item["adjusted_price"],
            average_price=item.get("average_price", -1.0),
        )
        result.append(prices)
    return result


def market_history(
    region_id: int,
    type_id: int,
    data: Sequence[dict[str, Any]],
) -> EAM.MarketHistory:
    """Import market history for a specific region and type from esi response."""
    result = EAM.MarketHistory(
        region_id=region_id,
        type_id=type_id,
        data=[
            EAM.MarketHistoryDetail(region_id=region_id, type_id=type_id, **x)
            for x in data
        ],
    )
    return result


def region_market_types_from_esi(
    paged_data: Sequence[Sequence[int]],
) -> Sequence[int]:
    """Import region market types from a sequence of integers."""
    # Flatten the list of lists into a single list of type IDs
    flat_data = list(chain(*paged_data))
    return flat_data


def region_market_orders_from_esi(
    region_id: int,
    paged_data: Sequence[Sequence[dict[str, Any]]],
) -> EAM.MarketOrdersByRegion:
    """Import market orders for a specific region from a sequence of dictionaries."""
    result = EAM.MarketOrdersByRegion(region_id=region_id, orders={})
    flattened_data = chain(*paged_data)
    for item in flattened_data:
        order = EAM.MarketOrder(region_id=region_id, **item)
        if order.type_id not in result.orders:
            result.orders[order.type_id] = EAM.MarketOrdersByType(
                region_id=region_id, type_id=order.type_id
            )
        if order.is_buy_order:
            result.orders[order.type_id].buy_orders.append(order)
        else:
            result.orders[order.type_id].sell_orders.append(order)
    return result


def region_and_type_market_orders_from_esi(
    region_id: int,
    type_id: int,
    paged_data: Sequence[Sequence[dict[str, Any]]],
) -> EAM.MarketOrdersByType:
    """Import market orders for a specific region and type from a sequence of dictionaries."""
    result = EAM.MarketOrdersByType(region_id=region_id, type_id=type_id)
    flattened_data = chain(*paged_data)
    for item in flattened_data:
        order = EAM.MarketOrder(region_id=region_id, **item)
        if order.is_buy_order:
            result.buy_orders.append(order)
        else:
            result.sell_orders.append(order)
    return result


def system_cost_indices_from_esi(
    data: Sequence[dict[str, Any]],
) -> EAM.SystemCostIndices:
    """Import system cost indices from a sequence of dictionaries."""
    result = EAM.SystemCostIndices(
        data_set_id=uuid4(),
        date=datetime.now(UTC).isoformat(),
        data={},
    )

    for item in data:
        system_id = item["solar_system_id"]
        result.data[system_id] = EAM.SystemCostIndex(
            system_id=system_id,
            manufacturing=item["manufacturing"],
            research_material=item["researching_material_efficiency"],
            research_time=item["researching_time_efficiency"],
            copying=item["copying"],
            invention=item["invention"],
            reaction=item["reaction"],
        )
    return result
