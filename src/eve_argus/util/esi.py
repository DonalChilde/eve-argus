"""Functions for use with Eve ESI data."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Literal, TypedDict

from pydantic import BaseModel

from eve_argus.models import argus as EAM
from eve_argus.models import esi as ED
from eve_argus.snippets.datetime.date_range import date_range_days


def summarize_market_history_by_periods(
    region_id: int,
    type_id: int,
    periods: Sequence[int],
    data: Sequence[EAM.MarketHistory],
) -> Sequence[EAM.MarketHistorySummary]:
    lookup = {date.fromisoformat(x.date): x for x in data}
    result: list[EAM.MarketHistorySummary] = []
    keys = list(lookup.keys())
    keys.sort(reverse=True)  # Sort by date descending
    most_recent = keys[0]
    for period in periods:
        dates = list(date_range_days(start_date=most_recent, days=period, past=True))
        end = dates[-1]
        summary = summarize_market_history_by_dates(dates=dates, data=lookup)
        summary.region_id = region_id
        summary.type_id = type_id
        summary.period = period
        summary.start = most_recent.isoformat()
        summary.end = end.isoformat()
        result.append(summary)
    return result


def summarize_market_history_by_dates(
    dates: Sequence[date], data: dict[date, EAM.MarketHistory]
) -> EAM.MarketHistorySummary:
    missing = average = highest = lowest = order_count = volume = 0
    count = len(dates)
    for key in dates:
        item = data.get(key, None)
        if item is None:
            missing += 1
            continue
        average = average + (item.average * item.volume)
        highest = highest + (item.highest * item.volume)
        lowest = lowest + (item.lowest * item.volume)
        order_count = order_count + item.order_count
        volume = volume + item.volume
    result = EAM.MarketHistorySummary(
        region_id=0,
        type_id=0,
        period=0,
        start="",
        end="",
        missing=missing,
        highest=highest / volume,
        average=average / volume,
        lowest=lowest / volume,
        order_count=int(order_count / count),
        volume=volume / count,
    )
    return result


def filter_orders(
    orders: Iterable[EAM.MarketOrder],
    type_id: int | None,
    is_buy_order: bool | None,
    location_id: int | None,
    location_spec: Literal["region", "system", "station"] | None,
) -> list[EAM.MarketOrder]:
    """Filter orders by type_id, is_buy_order, location_id, and location_spec.

    Args:
        orders (Iterable[EAM.MarketOrder]): _description_
        type_id (int | None): _description_
        is_buy_order (bool | None): _description_
        location_id (int | None): _description_
        location_spec (Literal["region", "system", "station"] | None): _description_

    Returns:
        list[EAM.MarketOrder]: _description_
    """
    filtered_orders = []
    if type_id is not None:
        filtered_orders = [order for order in orders if order.type_id == type_id]
    if is_buy_order is not None:
        filtered_orders = [
            order for order in filtered_orders if order.is_buy_order == is_buy_order
        ]
    if location_id is not None:
        if location_spec == "region":
            filtered_orders = [
                order for order in filtered_orders if order.region_id == location_id
            ]
        elif location_spec == "system":
            filtered_orders = [
                order for order in filtered_orders if order.system_id == location_id
            ]
        elif location_spec == "station":
            filtered_orders = [
                order for order in filtered_orders if order.location_id == location_id
            ]
        else:
            raise ValueError(
                "Invalid location_spec, do not filter by location_id. Did you give an id without a spec?"
            )
    return filtered_orders


class OrderSummaryTD(TypedDict):
    five_price: float
    """The price at which five percent of the available items can be transacted."""
    five_orders: int
    """The number of orders availablee at the five percent price."""
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


def _calculate_order_summary_TD(
    orders: Sequence[EAM.MarketOrder],
    is_buy_summary: bool,
    filter_factor: float = 100.0,
) -> OrderSummaryTD:
    """Calculate a summary of market orders.

    Assumes orders are already filtered by type_id, is_buy_order, and location.
    Also sorted by price ascending for sell orders and descending for buy orders.
    """
    five_price = lowest = highest = avg_price = 0.0
    total_items = total_orders = five_orders_count = 0
    five_items = filtered_items = filtered_orders = 0
    type_id_check: int = orders[0].type_id if orders else 0
    for order in orders:
        if order.is_buy_order != is_buy_summary:
            raise ValueError(
                f"All orders must be of the same type (buy/sell). {is_buy_summary=}"
            )
        if order.type_id != type_id_check:
            raise ValueError(
                f"All orders must be of the same type_id. {type_id_check=} {order.type_id=}"
            )
    if is_buy_summary:
        price_cutoff = orders[0].price / filter_factor if orders else 0.0
        valid_orders = [o for o in orders if o.price >= price_cutoff]
        excluded_orders = [o for o in orders if o not in valid_orders]
    else:
        price_cutoff = orders[0].price * filter_factor if orders else 0.0
        valid_orders = [o for o in orders if o.price <= price_cutoff]
        excluded_orders = [o for o in orders if o not in valid_orders]

    highest = max(o.price for o in valid_orders) if valid_orders else 0.0
    lowest = min(o.price for o in valid_orders) if valid_orders else 0.0
    total_volume = sum(o.volume_remain for o in valid_orders)
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
    five_percent_orders: list[EAM.MarketOrder] = []
    items = 0
    for order in valid_orders:
        if items <= five_percent_of_items:
            five_percent_orders.append(order)
            items += order.volume_remain
        else:
            break

    five_price = five_percent_orders[-1].price if five_percent_orders else 0.0
    five_orders = len(five_percent_orders)
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

    summary = OrderSummaryTD(
        five_price=five_price,
        five_orders=five_orders,
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


def calculate_order_summary(
    orders: list[EAM.MarketOrder],
    filter_factor: float,
    type_id: int,
    location_id: int,
    location_spec: Literal["region", "system", "station"] = "region",
) -> EAM.MarketOrderSummary:
    """Calculate an order summary.

    Args:
        orders (list[EAM.MarketOrder]): List of market orders to summarize.
        filter_factor (float): Factor to filter the orders by price.
        type_id (int): Type ID of the item.
        location_id (int): Location ID of the order summary.
        location_spec (Literal["region", "system", "station"]): Location specification for the order summary.

    Returns:
        EAM.MarketOrderSummary: Summary of the market orders.
    """
    filtered_orders = filter_orders(
        orders=orders,
        type_id=type_id,
        is_buy_order=None,
        location_id=location_id,
        location_spec=location_spec,
    )
    buy_orders = [order for order in filtered_orders if order.is_buy_order]
    sell_orders = [order for order in filtered_orders if not order.is_buy_order]
    buy_orders.sort(key=lambda x: x.price, reverse=True)
    sell_orders.sort(key=lambda x: x.price)
    buy_summary = _calculate_order_summary_TD(
        orders=buy_orders,
        is_buy_summary=True,
        filter_factor=filter_factor,
    )
    sell_summary = _calculate_order_summary_TD(
        orders=sell_orders,
        is_buy_summary=False,
        filter_factor=filter_factor,
    )

    summary = EAM.MarketOrderSummary(
        type_id=type_id,
        buy=EAM.MarketOrderSummaryDetails(
            type_id=type_id,
            is_buy_order=True,
            location_id=location_id,
            location_spec=location_spec,
            **buy_summary,
        ),
        sell=EAM.MarketOrderSummaryDetails(
            type_id=type_id,
            is_buy_order=False,
            location_id=location_id,
            location_spec=location_spec,
            **sell_summary,
        ),
    )
    return summary
