"""ESI return data models."""

from typing import TypedDict

class MarketHistory(TypedDict):
    """Market history data model."""
    average: float
    date: str
    highest: float
    lowest: float
    order_count: float
    volume: int
    
    
    
    
