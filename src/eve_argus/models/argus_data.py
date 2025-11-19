"""Models for the Argus app.

These models are derived from ESI and Static data.
"""

from datetime import date

from eve_argus.models.esi_data import (
    MarketHistory,
    Period,
    RegionId,
    SourcedFromESI,
    TypeId,
)
from eve_argus.snippets.datetime.date_range import date_range_days

from .helpers import BaseModelToDisk


class MarketHistorySummaryDetail(SourcedFromESI):
    """Market history summary data model."""

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

    @classmethod
    def from_market_history(
        cls, history: MarketHistory, period: int, start_date: date | None
    ) -> "MarketHistorySummaryDetail":
        """Create a MarketHistorySummaryDetail from MarketHistory data.

        When market history data is retrieved from ESI and made into a MarketHistory
        instance via the from_esi_response method, the dates in the data are sorted
        descending, so the most recent date is the first key in the data dictionary.
        This function relies on that assumption when start_date is None.

        Args:
            history (MarketHistory): The MarketHistory instance to summarize.
            period (int): The period in days to summarize.
            start_date (date | None): The start date of the summary range. if None,
                the most recent date in the data will be used.

        Returns:
            MarketHistorySummaryDetail: The summarized market history.
        """
        if start_date is None:
            dates = list(history.data.keys())
            start_date = dates[0]
        if start_date not in history.data:
            raise ValueError(f"Start date {start_date} not in market history data")
        dates = list(date_range_days(start_date=start_date, days=period, past=True))
        missing = average = highest = lowest = order_count = volume = 0
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
        summary = cls(
            region_id=history.region_id,
            type_id=history.type_id,
            period=period,
            start=start_date,
            end=dates[-1],
            missing=missing,
            highest=highest / volume,
            average=average / volume,
            lowest=lowest / volume,
            order_count=int(order_count / len(dates)),
            volume=volume / len(dates),
            last_modified=history.last_modified,
            expires=history.expires,
            retrieved=history.retrieved,
        )
        return summary


class MarketHistorySummmary(BaseModelToDisk):
    """Collection of market history summary details."""

    region_id: RegionId

    # Consider the best way to collect these. There is also date to consider.
    data: dict[tuple[RegionId, TypeId, Period], MarketHistorySummaryDetail]
