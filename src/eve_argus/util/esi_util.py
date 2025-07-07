from pathlib import Path
from typing import Any
from eve_argus.models import esi_data as ED
from eve_argus.models.market_history_summary import MarketHistorySummary
import csv
from datetime import date
from eve_argus.snippets.datetime.date_range import date_range_days


def market_history_summary(
    region_id: int, type_id: int, periods: list[int], data: list[ED.MarketHistory]
) -> dict[int, MarketHistorySummary]:
    lookup = {date.fromisoformat(x["date"]): x for x in data}
    result: dict[int, MarketHistorySummary] = {}
    keys = list(lookup.keys())
    keys.sort(reverse=True)  # Sort by date descending
    most_recent = keys[0]
    for period in periods:
        dates = list(date_range_days(start_date=most_recent, days=period, past=True))
        end = dates[-1]
        summary = generate_history_summary(dates=dates, data=lookup)
        summary["region_id"] = region_id
        summary["type_id"] = type_id
        summary["period"] = period
        summary["start"] = most_recent.isoformat()
        summary["end"] = end.isoformat()
        result[period] = summary
    return result


def generate_history_summary(
    dates: list[date], data: dict[date, ED.MarketHistory]
) -> MarketHistorySummary:
    missing = average = highest = lowest = order_count = volume = 0
    count = len(dates)
    for key in dates:
        item = data.get(key, None)
        if item is None:
            missing += 1
            continue
        average = average + (item["average"] * item["volume"])
        highest = highest + (item["highest"] * item["volume"])
        lowest = lowest + (item["lowest"] * item["volume"])
        order_count = order_count + item["order_count"]
        volume = volume + item["volume"]
    result = MarketHistorySummary(
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


def market_history_save_to_csv(
    region_id: int, type_id: int, data: list[ED.MarketHistory], dirpath: Path
) -> None:
    """Save market history data to a CSV file.

    Args:
        region_id (int): The ID of the region.
        type_id (int): The ID of the type.
        data (list[ED.MarketHistory]): List of market history data.
        dirpath (Path): The Path of the directory to save the data to.
    """
    filename = f"{region_id}_{type_id}_market_history.csv"
    filepath = dirpath / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    with filepath.open("w", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=ED.MarketHistory.__annotations__.keys()
        )
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)
