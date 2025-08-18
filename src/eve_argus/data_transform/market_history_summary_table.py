from collections.abc import Sequence
from typing import TypedDict

from eve_argus.models import argus as EAM


class HistorySummaryTD(TypedDict):
    region_id: int
    type_id: int
    period: int
    start: str
    end: str
    missing: int
    highest: float
    average: float
    lowest: float
    order_count: int
    volume: float
    last_modified: str


def market_history_summary_table(
    market_history: EAM.RegionalMarketHistorySummaries,
) -> Sequence[HistorySummaryTD]:
    result: list[HistorySummaryTD] = []
    for _, data in market_history.data.items():
        summary = HistorySummaryTD(
            region_id=data.region_id,
            type_id=data.type_id,
            period=data.period,
            start=data.start,
            end=data.end,
            missing=data.missing,
            highest=data.highest,
            average=data.average,
            lowest=data.lowest,
            order_count=data.order_count,
            volume=data.volume,
            last_modified=data.last_modified,
        )
        result.append(summary)
    return result
