"""ESI return data models."""

from typing import TypedDict


class MarketHistory(TypedDict):
    """Market history data model."""

    date: str
    highest: float
    average: float
    lowest: float
    order_count: float
    volume: int
