"""Functions for use with Eve ESI data."""

from pathlib import Path
from typing import Any
from collections.abc import Iterable, Sequence
from eve_argus.models import esi as ED
from eve_argus.models.argus import MarketHistorySummary, MarketHistory
import csv
from datetime import date
from eve_argus.snippets.datetime.date_range import date_range_days
from pydantic import BaseModel


def summarize_market_history_by_periods(
    region_id: int, type_id: int, periods: Sequence[int], data: Sequence[MarketHistory]
) -> Sequence[MarketHistorySummary]:
    lookup = {date.fromisoformat(x.date): x for x in data}
    result: list[MarketHistorySummary] = []
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
    dates: Sequence[date], data: dict[date, MarketHistory]
) -> MarketHistorySummary:
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


# def market_history_save_to_csv(
#     region_id: int, type_id: int, data: list[ED.MarketHistory], dirpath: Path
# ) -> None:
#     """Save market history data to a CSV file.

#     Args:
#         region_id (int): The ID of the region.
#         type_id (int): The ID of the type.
#         data (list[ED.MarketHistory]): List of market history data.
#         dirpath (Path): The Path of the directory to save the data to.
#     """
#     filename = f"{region_id}_{type_id}_market_history.csv"
#     filepath = dirpath / filename
#     filepath.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
#     with filepath.open("w", encoding="utf-8") as file:
#         writer = csv.DictWriter(
#             file, fieldnames=ED.MarketHistory.__annotations__.keys()
#         )
#         writer.writeheader()
#         for entry in data:
#             writer.writerow(entry)


# def pydantic_basemodel_to_csv(data: Iterable[BaseModel], filepath: Path) -> int:
#     filepath.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
#     data_iterator = iter(data)
#     count = 0
#     try:
#         first_item = next(data_iterator)
#         count += 1
#     except StopIteration:
#         return count
#     with filepath.open("w", encoding="utf-8") as file_out:
#         writer = csv.DictWriter(file_out,fieldnames=first_item.)


# def market_history_summary_save_to_csv(
#     data: Iterable[MarketHistorySummary], filepath: Path
# ) -> None:
#     """Save market history summary data to a CSV file.

#     Args:
#         data (Sequence[MarketHistorySummary]): List of market history data.
#         filepath (Path): The Path of the directory to save the data to.
#     """
#     filepath.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
#     with filepath.open("w", encoding="utf-8") as file:
#         # TODO write this as a general use Pydantic to csv function, top level only?
#         writer = csv.DictWriter(
#             file, fieldnames=ED.MarketHistory.__annotations__.keys()
#         )
#         writer.writeheader()
#         for entry in data:
#             writer.writerow(entry)
