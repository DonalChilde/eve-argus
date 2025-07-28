"""Functions for use with Eve ESI data."""

from collections.abc import Iterable, Sequence
from datetime import date

from eve_argus.models import argus as EAM
from eve_argus.snippets.datetime.date_range import date_range_days


def summarize_regional_market_history(
    history: EAM.MarketHistoryByRegion,
    type_ids: Iterable[int] | None = None,
    periods: Sequence[int] = (10, 30, 60, 90),
) -> EAM.MarketHistorySummariesByRegion:
    """Summarize market history by type."""
    if type_ids is None:
        type_ids = history.data.keys()
    region_id = history.region_id
    summaries = EAM.MarketHistorySummariesByRegion(
        region_id=region_id,
        data={},
    )
    for type_id in type_ids:
        market_history = history.data.get(type_id, None)
        if market_history is None:
            continue
        if not market_history.data:
            continue
        summary = summarize_market_history_by_periods(
            region_id=region_id,
            type_id=type_id,
            data=market_history.data,
            periods=periods,
        )
        summaries.data[type_id] = summary
    return summaries


def summarize_market_history_by_periods(
    region_id: int,
    type_id: int,
    periods: Sequence[int],
    data: Sequence[EAM.MarketHistoryDetail],
) -> dict[int, EAM.MarketHistorySummary]:
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
    return {x.period: x for x in result}


def summarize_market_history_by_dates(
    dates: Sequence[date], data: dict[date, EAM.MarketHistoryDetail]
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
