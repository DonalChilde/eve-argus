"""Models for the Argus app.

These models are derived from ESI and Static data.
"""

from datetime import date
from typing import Literal, Self

from pydantic import BaseModel

from eve_argus.calculations.calculate_history_summary import (
    HistorySummaryDict,
    calculate_history_summary,
)
from eve_argus.calculations.calculate_order_summary import calculate_order_summary
from eve_argus.old_models.esi_data import (
    MarketHistory,
    MarketOrders,
    Period,
    RegionalMarketOrders,
    RegionId,
    SourcedFromESI,
    TypeId,
)

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
    ) -> Self:
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
        summary_dict: HistorySummaryDict = calculate_history_summary(
            history=history, period=period, start_date=start_date
        )
        summary = cls(
            **summary_dict,
            last_modified=history.last_modified,
            expires=history.expires,
            retrieved=history.retrieved,
        )
        return summary


class MarketHistorySummmaries(BaseModelToDisk):
    """Collection of market history summary details."""

    region_id: RegionId
    period: Period
    start_date: date
    data: dict[TypeId, MarketHistorySummaryDetail]

    @classmethod
    def from_market_histories(
        cls,
        histories: list[MarketHistory],
        region_id: RegionId,
        period: Period,
        start_date: date,
    ) -> Self:
        """Create MarketHistorySummmaries from a collection of MarketHistory instances.

        Histories must all be for the same region ID.

        Args:
            histories (list[MarketHistory]): The market histories to summarize.
            region_id (RegionId): The region ID for the summaries.
            period (Period): The period in days for the summaries.
            start_date (date): The start date for the summaries.

        Returns:
            MarketHistorySummmaries: The collection of market history summaries.
        """
        data: dict[TypeId, MarketHistorySummaryDetail] = {}
        for history in histories:
            if history.region_id != region_id:
                msg = (
                    f"Region ID mismatch: expected {region_id}, "
                    f"got {history.region_id=} for type ID {history.type_id=}"
                )
                raise ValueError(msg)
            summary = MarketHistorySummaryDetail.from_market_history(
                history=history, period=period, start_date=start_date
            )
            data[history.type_id] = summary
        start_date_resolved = data[next(iter(data))].start
        return cls(
            data=data,
            period=period,
            start_date=start_date_resolved,
            region_id=region_id,
        )


class MarketOrderSummaryDetail(BaseModel):
    """Details of a market order summary for a specific type and location."""

    type_id: int
    """The type ID of the item."""
    is_buy_summary: bool
    """True if this summary is for buy orders, False for sell orders."""
    location_id: int
    """The location ID of the order summary. This could be a region, system, or station ID."""
    location_spec: Literal["region", "system", "station"] = "region"
    """The location specification for the order summary."""
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

    @classmethod
    def from_market_orders(
        cls,
        orders: MarketOrders,
        is_buy_summary: bool,
        location_id: int | None = None,
        location_spec: Literal["region", "system", "station"] = "region",
    ) -> Self:
        """Create a MarketOrderSummaryDetail for buy or sell orders from MarketOrders data.

        Args:
            orders (MarketOrders): The MarketOrders instance to summarize.
            is_buy_summary (bool): True to summarize buy orders, False for sell orders.
            location_id (int | None): The location ID to filter orders by.
                If None, no location filtering is applied. Defaults to None.
            location_spec (Literal["region", "system", "station"]): The location specification
                for the summary. Defaults to "region".
        """
        if location_id is None:
            location_id = orders.region_id
            location_spec = "region"
        filtered_orders = orders.filter_orders(
            is_buy_order=is_buy_summary,
            location_id=location_id,
            location_spec=location_spec,
        )
        summary_dict = calculate_order_summary(
            filtered_orders, is_buy_summary=is_buy_summary
        )
        summary = cls(
            **summary_dict,
            location_id=location_id,
            location_spec=location_spec,
        )
        return summary


class MarketOrderSummary(BaseModel):
    buy_summary: MarketOrderSummaryDetail
    """Summary details for buy orders."""
    sell_summary: MarketOrderSummaryDetail
    """Summary details for sell orders."""
    type_id: TypeId
    """The type ID of the item."""
    location_id: int
    """The location ID of the order summary."""
    location_spec: Literal["region", "system", "station"] = "region"
    """The location specification for the order summary."""

    @classmethod
    def from_market_orders(
        cls,
        orders: MarketOrders,
        location_id: int | None = None,
        location_spec: Literal["region", "system", "station"] = "region",
    ) -> Self:
        """Create a MarketOrderSummary from MarketOrders data.

        Args:
            orders (MarketOrders): The MarketOrders instance to summarize.
            location_id (int | None): The location ID to filter orders by.
                If None, no location filtering is applied. Defaults to None.
            location_spec (Literal["region", "system", "station"]): The location specification
                for the summary. Defaults to "region".

        Returns:
            MarketOrderSummary: The market order summary.
        """
        if location_id is None:
            location_id = orders.region_id
            location_spec = "region"
        buy_summary = MarketOrderSummaryDetail.from_market_orders(
            orders,
            is_buy_summary=True,
            location_id=location_id,
            location_spec=location_spec,
        )
        sell_summary = MarketOrderSummaryDetail.from_market_orders(
            orders,
            is_buy_summary=False,
            location_id=location_id,
            location_spec=location_spec,
        )
        summary = cls(
            type_id=orders.type_id,
            location_id=location_id,
            location_spec=location_spec,
            buy_summary=buy_summary,
            sell_summary=sell_summary,
        )
        return summary


class RegionalMarketOrderSummaries(SourcedFromESI):
    """Collection of market order summaries for a specific region."""

    region_id: RegionId
    """The region ID for the market order summaries."""
    location_id: int
    """The location ID for the market order summaries."""
    location_spec: Literal["region", "system", "station"] = "region"
    """The location specification for the market order summaries."""
    data: dict[TypeId, MarketOrderSummary]
    """The market order summaries keyed by type ID."""

    @classmethod
    def from_regional_market_orders(
        cls,
        orders: RegionalMarketOrders,
        location_id: int | None = None,
        location_spec: Literal["region", "system", "station"] = "region",
    ) -> Self:
        """Create RegionalMarketOrderSummaries from MarketOrders data.

        Args:
            orders (RegionalMarketOrders): The RegionalMarketOrders instance to summarize.
            location_id (int | None): The location ID to filter orders by.
                If None, no location filtering is applied. Defaults to None.
            location_spec (Literal["region", "system", "station"]): The location specification
                for the summary. Defaults to "region".

        Returns:
            RegionalMarketOrderSummaries: The collection of market order summaries.
        """
        if location_id is None:
            location_id = orders.region_id
            location_spec = "region"
        data: dict[TypeId, MarketOrderSummary] = {}
        for type_id, market_orders in orders.data.items():
            summary = MarketOrderSummary.from_market_orders(
                market_orders,
                location_id=location_id,
                location_spec=location_spec,
            )
            data[type_id] = summary
        summaries = cls(
            region_id=orders.region_id,
            location_id=location_id,
            location_spec=location_spec,
            data=data,
            last_modified=orders.last_modified,
            expires=orders.expires,
            retrieved=orders.retrieved,
        )
        return summaries
