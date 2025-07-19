from collections.abc import Sequence
from itertools import chain
from typing import Any

from eve_argus.models import argus as EAM
from eve_argus.models.esi import EsiResponse


def market_prices_universe_from_esi(
    data: Sequence[dict[str, Any]],
) -> Sequence[EAM.MarketPricesUniverse]:
    """Import market prices for the universe from a sequence of dictionaries."""
    result: list[EAM.MarketPricesUniverse] = []
    for item in data:
        prices = EAM.MarketPricesUniverse(
            type_id=item["type_id"],
            adjusted_price=item["adjusted_price"],
            average_price=item.get("average_price", -1.0),
        )
        result.append(prices)
    return result


def market_history_from_esi(
    region_id: int,
    type_id: int,
    response: EsiResponse,
) -> EAM.MarketHistoryByType:
    """Import market history for a specific region and type from esi response."""
    result = EAM.MarketHistoryByType(
        region_id=region_id,
        type_id=type_id,
        data=[EAM.MarketHistoryDetail(**x) for x in response.data],
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
