"""Functions for use with Eve ESI data."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from collections.abc import Iterable, Sequence
from eve_argus.models import esi as ED
from eve_argus.models import argus as EAM
from datetime import date
from eve_argus.snippets.datetime.date_range import date_range_days
from pydantic import BaseModel


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


def calculate_order_summary(
    orders: dict[int, Sequence[EAM.MarketOrder]],
) -> EAM.MarketOrderSummary:
    """Calculate a summary of market orders."""
    # input data is a dict of market orders for one region, grouped by type_id.
    # Group orders by type_id -> region -> system.
    # calculate summaries for region and system.
    # allow restriction to a single system? Do this higher up.

    # Calculate the 5% percentile for buy and sell orders.
    # Percentile is calculated by removing outliers from the volume calculations,
    # highest buy / 100), (lowest sell * 100) then finding the first order price that
    # is equal or greater than the 5% of the total available volume.

    highest_buy = lowest_sell = 0.0
    total_volume = 0.0
    for order in orders:
        if order.is_buy_order:
            if order.price > highest_buy:
                highest_buy = order.price
        else:
            if lowest_sell == 0.0 or order.price < lowest_sell:
                lowest_sell = order.price
        total_volume += order.volume_remain
    if lowest_sell == 0.0:
        lowest_sell = highest_buy
    summary = EAM.MarketOrderSummary(
        highest_buy=highest_buy,
        lowest_sell=lowest_sell,
        total_volume=total_volume,
        percentile_buy=highest_buy / 100,
        percentile_sell=lowest_sell * 100,
        buy_5=highest_buy,
        sell_5=lowest_sell,
        buy_5_volume=0,
        sell_5_volume=0,
        region_id=0,
        system_id=0,
        type_id=0,
        average_price=(highest_buy + lowest_sell) / 2,
        order_count=len(orders),
    )
    return summary
