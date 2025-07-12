"""Functions for use with Eve ESI data."""

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


def import_market_prices_universe(
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
