"""Function to calculate order summary statistics."""

from collections.abc import Sequence
from typing import TypedDict

from eve_argus.old_models.esi_data import MarketOrderDetail


class OrderSummaryDict(TypedDict):
    """TypedDict for order summary details."""

    type_id: int
    """The type ID of the item."""
    is_buy_summary: bool
    """Whether the summary is for buy orders."""
    five_price: float
    """The price at which five percent of the available items can be transacted."""
    five_orders: int
    """The number of orders available at the five percent price."""
    five_items: int
    """The number of items available at the five percent price."""
    lowest: float
    """The lowest price."""
    highest: float
    """The highest price."""
    total_items: int
    """The total number of items available."""
    total_orders: int
    """The total number of orders."""
    avg_price: float
    """The average price of the available items."""
    filtered_items: int
    """The number of items that did not meet the threshold."""
    filtered_orders: int
    """The number of orders that did not meet the threshold."""


def calculate_order_summary(
    orders: Sequence[MarketOrderDetail],
    is_buy_summary: bool,
    filter_factor: float = 100.0,
) -> OrderSummaryDict:
    """Calculate a summary of market orders.

    Assumes orders are already filtered by type_id and is_buy_order, as well as
    location if desired.

    Args:
        orders: A sequence of MarketOrderDetail objects to summarize. Should be
            pre-filtered by type_id and is_buy_order, and optionally by location.
        is_buy_summary: If True, summarize buy orders.
            If False, summarize sell orders.
        filter_factor: Factor used to filter outlier orders. For buy orders, only
            orders with price >= (highest_price / filter_factor) are included.
            For sell orders, only orders with price <= (lowest_price * filter_factor)
            are included. Defaults to 100.0.

    Returns:
        OrderSummaryDict containing:
            - type_id: The item type ID of the orders
            - is_buy_summary: Whether this is a buy or sell summary
            - five_price: The price at the 5% volume threshold
            - five_orders: Number of orders in the top 5% by volume
            - five_items: Total volume at or better than five_price
            - lowest: Lowest price among valid orders
            - highest: Highest price among valid orders
            - total_items: Total volume of all valid orders
            - total_orders: Count of valid orders
            - avg_price: Volume-weighted average price of valid orders
            - filtered_items: Total volume of filtered/excluded orders
            - filtered_orders: Count of filtered/excluded orders

    Raises:
        ValueError: If orders contain mismatched is_buy_order values or multiple
            type_ids.

    Note:
        The function calculates the "five percent" metrics by accumulating orders
        from the best price until reaching 5% of the total volume, then determining
        the price and volume at that threshold.
    """
    if is_buy_summary:
        orders = sorted(orders, key=lambda o: o.price, reverse=True)
    else:
        orders = sorted(orders, key=lambda o: o.price)
    five_price = lowest = highest = avg_price = 0.0
    total_items = total_orders = five_orders_count = 0
    five_items = filtered_items = filtered_orders = 0

    # Check that all orders have the same is_buy_order and type_id
    type_id_check: int = orders[0].type_id if orders else 0
    for order in orders:
        if order.is_buy_order != is_buy_summary:
            msg = f"Order is_buy_order {order.is_buy_order} does not match summary type {is_buy_summary}"
            raise ValueError(msg)
        if order.type_id != type_id_check:
            msg = "All orders must be of the same type_id."
            raise ValueError(msg)

    # Filter out outlier orders based on filter_factor
    if is_buy_summary:
        price_cutoff = orders[0].price / filter_factor if orders else 0.0
        valid_orders = [o for o in orders if o.price >= price_cutoff]
        excluded_orders = [o for o in orders if o.price < price_cutoff]
    else:
        price_cutoff = orders[0].price * filter_factor if orders else 0.0
        valid_orders = [o for o in orders if o.price <= price_cutoff]
        excluded_orders = [o for o in orders if o.price > price_cutoff]
    highest = max(o.price for o in valid_orders) if valid_orders else 0.0
    lowest = min(o.price for o in valid_orders) if valid_orders else 0.0
    total_volume = sum(o.volume_remain for o in valid_orders)
    # Calculate volume-weighted average price
    avg_price = (
        sum(o.volume_remain * o.price for o in valid_orders) / total_volume
        if valid_orders
        else 0.0
    )
    total_items = sum(o.volume_remain for o in valid_orders)
    total_orders = len(valid_orders)
    filtered_items = sum(o.volume_remain for o in excluded_orders)
    filtered_orders = len(excluded_orders)
    five_percent_of_items = total_items * 0.05
    five_percent_orders: list[MarketOrderDetail] = []
    items = 0
    for order in valid_orders:
        if items <= five_percent_of_items:
            five_percent_orders.append(order)
            items += order.volume_remain
        else:
            break

    five_price = five_percent_orders[-1].price if five_percent_orders else 0.0
    five_orders_count = len(five_percent_orders)
    if is_buy_summary:
        # For buy orders, we want the total volume of items at or above the five_price
        five_items = (
            sum(o.volume_remain for o in five_percent_orders if o.price >= five_price)
            if five_percent_orders
            else 0
        )
    else:
        # For sell orders, we want the total volume of items at or below the five_price
        five_items = (
            sum(o.volume_remain for o in valid_orders if o.price <= five_price)
            if five_percent_orders
            else 0
        )

    summary = OrderSummaryDict(
        type_id=type_id_check,
        is_buy_summary=is_buy_summary,
        five_price=five_price,
        five_orders=five_orders_count,
        five_items=five_items,
        lowest=lowest,
        highest=highest,
        total_items=total_items,
        total_orders=total_orders,
        avg_price=avg_price,
        filtered_items=filtered_items,
        filtered_orders=filtered_orders,
    )

    return summary
