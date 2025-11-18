"""Models derived from data from the EVE Esi."""

from pydantic import BaseModel

from . import static_data as SD
from .helpers import BaseModelToDisk

# Use type aliases for better readability IN TYPE HINTS.
type RegionId = int
type TypeId = int
type Period = int


class MarketHistorySummary(BaseModel):
    """Market history summary data model."""

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
    """The UTC datetime that is the last_modified of the source data, in ISO 8601 format."""


class MarketHistorySummmaries(BaseModelToDisk):
    """Collection of market history summaries."""

    # Consider the best way to collect these. There is also date to consider.
    data: dict[tuple[RegionId, TypeId, Period], MarketHistorySummary]
    # info: SD.SdeInfo
