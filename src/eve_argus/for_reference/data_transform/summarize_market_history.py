"""Functions for manipulating MarketHistory."""

from collections.abc import Iterable, Sequence
from datetime import date
from uuid import uuid4

from eve_argus.models import argus as EAM
from eve_argus.snippets.datetime.date_range import date_range_days

# TODO re think how multiple summary periods might work.
# Given keeping the raw data is kinda feasible, it is more practical to generate summaries one at a time.


def summarize_regional_market_history(
    histories: EAM.RegionalMarketHistory,
    type_ids: Iterable[int] | None = None,
    periods: Sequence[int] = (10, 30, 60, 90),
) -> EAM.RegionalMarketHistorySummaries:
    """Summarize market history by type and period of days.

    Args:
        histories: The market histories to summarize.
        type_ids: Optional list of type IDs to summarize. If None, all type_ids are summarized.
        periods: The periods in days to summarize the market history.

    Returns:
        EAM.MarketHistorySummaries: The summarized market history.
    """
    if type_ids is None:
        type_ids = histories.data.keys()
    region_id = histories.region_id
    summaries = EAM.RegionalMarketHistorySummaries(
        data_set_id=uuid4(),
        region_id=region_id,
        data={},
    )
    for type_id in type_ids:
        market_history = histories.data.get(type_id, None)
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
        first_period = periods[0]
        summaries.data[type_id] = summary[first_period]
    return summaries


def summarize_market_history_by_periods(
    region_id: int,
    type_id: int,
    periods: Sequence[int],
    data: Sequence[EAM.MarketHistoryDetail],
) -> dict[int, EAM.MarketHistorySummary]:
    """Summarize market history by periods.

    Periods count back from most recent date.

    Args:
        region_id (int): The region ID.
        type_id (int): The type ID.
        periods (Sequence[int]): The periods in days to summarize.
        data (Sequence[EAM.MarketHistoryDetail]): The market history data.

    Returns:
        dict[int, EAM.MarketHistorySummary]: The summarized market history by period.
    """
    by_date = {date.fromisoformat(x.date): x for x in data}
    result: list[EAM.MarketHistorySummary] = []
    keys = list(by_date.keys())
    keys.sort(reverse=True)  # Sort by date descending
    most_recent = keys[0]
    for period in periods:
        dates = list(date_range_days(start_date=most_recent, days=period, past=True))
        end = dates[-1]
        summary = summarize_market_history_by_dates(dates=dates, data=by_date)
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
    """Summarize market history by dates.

    Args:
        dates (Sequence[date]): The dates to summarize.
        data (dict[date, EAM.MarketHistoryDetail]): The market history data keyed by date.

    Returns:
        EAM.MarketHistorySummary: The summarized market history.
    """
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
        last_modified="",
    )
    return result
