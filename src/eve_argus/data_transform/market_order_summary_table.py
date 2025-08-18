from collections.abc import Sequence
from typing import Literal, TypedDict

from eve_argus.models import argus as EAM


class MarketOrderSummaryTD(TypedDict):
    type_id: int
    """The type ID of the item."""
    location_id: int
    """The location ID of the order summary."""
    location_spec: Literal["region", "system", "station"]
    """The location specification for the order summary."""
    buy_five_price: float
    """The price at which five percent of the available items can be transacted."""
    buy_five_orders: int
    """The number of orders availablee at the five percent price."""
    buy_five_items: int
    """The number of items available at the five percent price."""
    buy_lowest: float
    """The lowest price."""
    buy_highest: float
    """The highest price."""
    buy_total_items: int
    """The total number of items available."""
    buy_total_orders: int
    """The total number of orders."""
    buy_avg_price: float
    """The average price of the available items."""
    buy_filtered_items: int
    """The number of items that did not meet the threshold."""
    buy_filtered_orders: int
    """The number of orders that did not meet the threshold."""
    sell_five_price: float
    """The price at which five percent of the available items can be transacted."""
    sell_five_orders: int
    """The number of orders availablee at the five percent price."""
    sell_five_items: int
    """The number of items available at the five percent price."""
    sell_lowest: float
    """The lowest price."""
    sell_highest: float
    """The highest price."""
    sell_total_items: int
    """The total number of items available."""
    sell_total_orders: int
    """The total number of orders."""
    sell_avg_price: float
    """The average price of the available items."""
    sell_filtered_items: int
    """The number of items that did not meet the threshold."""
    sell_filtered_orders: int
    """The number of orders that did not meet the threshold."""


def market_order_summary_table(
    market_orders: EAM.MarketOrderSummaries,
) -> Sequence[MarketOrderSummaryTD]:
    result: list[MarketOrderSummaryTD] = []
    for _, data in market_orders.data.items():
        summary = MarketOrderSummaryTD(
            type_id=data.type_id,
            location_id=data.location_id,
            location_spec=data.location_spec,
            buy_five_price=data.buy.five_price,
            buy_five_orders=data.buy.five_orders,
            buy_five_items=data.buy.five_items,
            buy_lowest=data.buy.lowest,
            buy_highest=data.buy.highest,
            buy_total_items=data.buy.total_items,
            buy_total_orders=data.buy.total_orders,
            buy_avg_price=data.buy.avg_price,
            buy_filtered_items=data.buy.filtered_items,
            buy_filtered_orders=data.buy.filtered_orders,
            sell_five_price=data.sell.five_price,
            sell_five_orders=data.sell.five_orders,
            sell_five_items=data.sell.five_items,
            sell_lowest=data.sell.lowest,
            sell_highest=data.sell.highest,
            sell_total_items=data.sell.total_items,
            sell_total_orders=data.sell.total_orders,
            sell_avg_price=data.sell.avg_price,
            sell_filtered_items=data.sell.filtered_items,
            sell_filtered_orders=data.sell.filtered_orders,
        )
        result.append(summary)
    return result
