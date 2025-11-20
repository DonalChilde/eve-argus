from datetime import date
from typing import TypedDict

from eve_argus.models.esi_data import MarketHistory, Period
from eve_argus.snippets.datetime.date_range import date_range_days


class HistorySummaryDict(TypedDict):
    region_id: int
    type_id: int
    period: int
    start: date
    end: date
    missing: int
    highest: float
    average: float
    lowest: float
    order_count: int
    volume: float


def calculate_history_summary(
    history: MarketHistory,
    period: Period,
    start_date: date | None = None,
) -> HistorySummaryDict:
    """Calculate a summary of a MarketHistory over a specified period.

    Args:
        history (MarketHistory): The market history to summarize.
        period (Period): The period in days for the summary.
        start_date (date | None): The start date for the summary. If None,
            the most recent date in the history will be used.

    Returns:
        HistorySummaryDict: The summarized market history data.
    """
    if start_date is None:
        start_date = next(iter(history.data.keys()))
    if start_date not in history.data:
        raise ValueError(f"Start date {start_date} not in market history data")
    dates = list(date_range_days(start_date=start_date, days=period, past=True))
    missing = order_count = 0
    average = highest = lowest = volume = 0.0
    for date_key in dates:
        item = history.data.get(date_key, None)
        if item is None:
            missing += 1
            continue
        average = average + (item.average * item.volume)
        highest = highest + (item.highest * item.volume)
        lowest = lowest + (item.lowest * item.volume)
        order_count = order_count + item.order_count
        volume = volume + item.volume
    summary: HistorySummaryDict = {
        "region_id": history.region_id,
        "type_id": history.type_id,
        "period": period,
        "start": start_date,
        "end": dates[-1],
        "missing": missing,
        "highest": highest / volume if volume > 0 else 0.0,
        "average": average / volume if volume > 0 else 0.0,
        "lowest": lowest / volume if volume > 0 else 0.0,
        "order_count": int(order_count / len(dates)) if len(dates) > 0 else 0,
        "volume": volume / len(dates) if len(dates) > 0 else 0.0,
    }
    return summary
