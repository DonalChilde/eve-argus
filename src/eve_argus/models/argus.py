"""Models for the Eve Argus app."""

from collections.abc import Sequence
from enum import Enum, StrEnum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class DataTypes(StrEnum):
    """Data types for Argus."""

    # This is to enable different actions based on the type of data
    ## e.g. different expiration times for market history vs market pricing.
    UniverseMarketPrices = "universe_market_prices"
    RegionalMarketOrders = "regional_market_orders"
    MarketOrderSummaries = "market_order_summaries"
    SystemCostIndices = "system_cost_indices"
    TypeIDSubsets = "type_id_subsets"
    Static = "static"
    Blueprints = "blueprints"
    TypeInfos = "type_infos"
    TypeDescriptions = "type_descriptions"
    MetaGroups = "meta_groups"
    Groups = "groups"
    Categories = "categories"
    MarketGroups = "market_groups"
    MarketHistory = "market_history"
    MarketHistorySummaries = "market_history_summaries"
    RegionalMarketTypes = "regional_market_types"


# etag: "d74ee14547cb1f6b1ee73e40c354bd72f3b35041220920dfd9170023"
# expires: Mon, 04 Aug 2025 19:43:16 GMT
# last-modified: Mon, 04 Aug 2025 18:43:16 GMT


class TopLevelDataSet(BaseModel):
    """A top-level data set model for Argus."""

    data_set_id: UUID
    """The unique identifier for the data set."""
    last_modified: str | None = None
    """The last modified date of the data set, in ISO 8601 format."""
    etag: str | None = None
    """The ETag for the data set, used for caching and validation."""
    expires: str | None = None
    """The expiration date of the data set, in ISO 8601 format."""
    description: str | None = None
    """An optional description of the data set."""
    data_type: DataTypes
    """The type of data contained in this data set."""
    data_source_type: Literal["esi_api", "esi_cache", "sde", "not_set"] = "not_set"
    data_source: UUID | None = None
    """The source of the data, if applicable, as a UUID."""


class RegionalMarketTypes(TopLevelDataSet):
    """A collection of type IDs for items available in the market in a specific region."""

    region_id: int
    """The region ID where the market types are located."""
    type_ids: set[int] = Field(default_factory=set)
    """A set of type IDs available in the market in the specified region."""


class TypeIDSubset(BaseModel):
    """A subset of type IDs."""

    description: str
    type_ids: set[int]
    """A set of type IDs."""


class TypeIDSubsets(TopLevelDataSet):
    """A collection of type ID subsets.

    These subsets are mostly built from SDE static data.
    """

    published: TypeIDSubset
    """The published type ID subset."""
    blueprints: TypeIDSubset
    """The type_ids of published blueprints."""
    manufacturing_materials: TypeIDSubset
    """The type_ids of published items that can be used as manufacturing materials."""
    copy_materials: TypeIDSubset
    """The type_ids of published items that can be used as copying materials."""
    invention_materials: TypeIDSubset
    """The type_ids of published items that can be used as invention materials."""
    reaction_materials: TypeIDSubset
    """The type_ids of published items that can be used as reaction materials."""
    research_materials: TypeIDSubset
    """The type_ids of published items that can be used as research materials for TE or ME."""
    manufacturing_products: TypeIDSubset
    """The type_ids of published items that can be manufactured."""
    reaction_products: TypeIDSubset
    """The type_ids of published items that can be produced by reactions."""
    industry_related: TypeIDSubset
    """A union of all type_ids that are related to industry activities."""

    types_in_market: TypeIDSubset
    """The type_ids of published items that exist in the market."""


class SystemCostIndex(BaseModel):
    """System cost index data model."""

    system_id: int
    """The solar system ID."""
    manufacturing: float
    """The manufacturing cost index."""
    research_material: float
    """The research material cost index."""
    research_time: float
    """The research time cost index."""
    copying: float
    """The copying cost index."""
    invention: float
    """The invention cost index."""
    reaction: float
    """The reaction cost index."""


class SystemCostIndices(TopLevelDataSet):
    """The cost indices for all solar systems."""

    data: dict[int, SystemCostIndex]
    """A dictionary mapping solar system IDs to their cost indices."""


class MarketHistoryDetail(BaseModel):
    """Market history data model."""

    region_id: int
    """The region ID where the market history is located."""
    type_id: int
    """The type ID of the item."""
    date: str
    highest: float
    average: float
    lowest: float
    order_count: float
    volume: int


class MarketHistory(TopLevelDataSet):
    """Market history for a specific region and type."""

    region_id: int
    """The region ID where the market history is located."""
    type_id: int
    """The type ID of the item."""
    data: Sequence[MarketHistoryDetail]
    """A sequence of market history records."""


class RegionalMarketHistory:
    """A collection of market history records for a specific region."""

    region_id: int
    """The region ID where the market history is located."""
    data: dict[int, MarketHistory]
    """A dictionary mapping type IDs to market history records for that region."""


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


class RegionalMarketHistorySummaries(TopLevelDataSet):
    """A collection of the most recent market history summaries.

    Summaries may have different effective dates, but they are all for the same region.
    """

    region_id: int
    """The region ID where the market history summaries are located."""
    data: dict[int, MarketHistorySummary] = {}
    """A dictionary mapping type IDs to market history summaries."""


class Activity_Name(Enum):
    manufacturing = 1
    research_time = 3
    research_material = 4
    copying = 5
    invention = 8
    reaction = 11


class Material(BaseModel):
    quantity: int
    type_id: int = Field(
        validation_alias="typeID", description="The type ID of the material."
    )


class Skill(BaseModel):
    level: int
    type_id: int = Field(
        validation_alias="typeID", description="The type ID of the material."
    )


class Activity(BaseModel):
    materials: list[Material] = []
    products: list[Material] = []
    skills: list[Skill] = []
    time: int


class Activities(BaseModel):
    copying: Activity | None = None
    manufacturing: Activity | None = None
    research_material: Activity | None = None
    research_time: Activity | None = None
    reaction: Activity | None = None
    invention: Activity | None = None


class Blueprint(BaseModel):
    blueprintTypeID: int
    maxProductionLimit: int
    activities: Activities


class Blueprints(TopLevelDataSet):
    """A collection model to make serialization faster."""

    data: dict[int, Blueprint]


class TypeInfo(BaseModel):
    name: str
    type_id: int
    group_id: int | None
    """The group ID of the item, None if not available."""
    category_id: int | None
    """The category ID of the item, None if not available."""
    market_group_id: int | None
    meta_group_id: int | None
    graphic_id: int | None
    capacity: float | None
    portion_size: int  # -1 if no value in SDE
    """The portion size of the item, -1 if not available."""
    published: bool


class TypeInfos(TopLevelDataSet):
    """A collection model to make serialization faster."""

    data: dict[int, TypeInfo]


class TypeDescription(BaseModel):
    type_id: int
    description: str


class TypeDescriptions(TopLevelDataSet):
    """A collection model to make serialization faster."""

    data: dict[int, TypeDescription]


class MetaGroup(BaseModel):
    meta_id: int
    name: str


class MetaGroups(TopLevelDataSet):
    """A collection model to make serialization faster."""

    data: dict[int, MetaGroup]


class Group(BaseModel):
    group_id: int
    anchorable: bool
    anchored: bool
    category_id: int
    fittable_non_singleton: bool
    icon_id: int  # -1 if no value in sde
    name: str
    published: bool
    use_base_price: bool


class Groups(TopLevelDataSet):
    data: dict[int, Group]


class Category(BaseModel):
    category_id: int
    name: str
    published: bool


class Categories(TopLevelDataSet):
    data: dict[int, Category]


class MarketGroup(BaseModel):
    group_id: int
    """The unique identifier for the market group."""
    name: str
    """The name of the market group."""
    description: str
    """The description of the market group, empty if not available."""
    has_types: bool
    """True if this group contains types."""
    icon_id: int
    """The icon ID for the market group, -1 if not available."""
    path: tuple[int, ...]
    """The path is a tuple of market group IDs leading to this group, including the current group."""


class MarketGroups(TopLevelDataSet):
    """A collection model to make serialization faster."""

    data: dict[int, MarketGroup]

    def path_string(self, group_ids: Sequence[int], separator: str = r"\\") -> str:
        """Create a string representation of the market group path."""
        return f"{separator}".join(
            str(self.data[group_id].name)
            for group_id in group_ids
            if group_id in self.data
        )


class UniverseMarketPrice(BaseModel):
    """Universe Market prices data model."""

    type_id: int
    """The type ID of the item."""
    adjusted_price: float
    """The adjusted price of the item, -1.0 if not available."""
    average_price: float
    """The average price of the item, -1.0 if not available."""


class UniverseMarketPrices(TopLevelDataSet):
    """A collection of universe pricing."""

    data: dict[int, UniverseMarketPrice]
    """A dictionary mapping type IDs to adjusted and average market prices for the universe."""


class MarketOrderDetail(BaseModel):
    """A market order data model."""

    duration: int  # in days
    is_buy_order: bool  # True for buy orders, False for sell orders
    issued: str  # ISO 8601 date string
    location_id: int  # The location ID where the order is placed
    min_volume: int  # Minimum volume that must be bought/sold
    order_id: int  # Unique identifier for the order
    price: float  # Price per unit
    range: str  # e.g., 'region', 'solar_system', 'station'
    region_id: int  # The region ID where the order is placed
    system_id: int  # The solar system ID where the order is placed
    type_id: int  # The type ID of the item being ordered
    volume_total: int  # Total volume of the order
    volume_remain: int  # Remaining volume of the order


class MarketOrders(BaseModel):
    """A collection model for buy and sell market orders for one type in one region."""

    region_id: int
    """The region ID where the market orders are located."""
    type_id: int
    """The type ID of the market orders."""
    buy_orders: list[MarketOrderDetail] = []
    """A list of market buy orders for the specified type."""
    sell_orders: list[MarketOrderDetail] = []
    """A list of market sell orders for the specified type."""


class RegionalMarketOrders(TopLevelDataSet):
    """A collection model for market orders multiple types in a specific region.

    The most efficient way to get market orders from esi is to request all orders for a region at once.
    That makes this the default representation for storage of market orders in a region.
    """

    region_id: int
    """The region ID where the market orders are located."""
    orders: dict[int, MarketOrders] = {}
    """A dictionary mapping type IDs to market orders for that region."""


class MarketOrderSummaryDetails(BaseModel):
    """Details of a market order summary for a specific type and location."""

    type_id: int
    """The type ID of the item."""
    is_buy_order: bool
    """True if this summary is for buy orders, False for sell orders."""
    location_id: int
    """The location ID of the order summary."""
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


class MarketOrderSummary(BaseModel):
    """Summary of market orders for a specific type."""

    type_id: int
    """The type ID of the item for which the summary is calculated."""
    location_spec: Literal["region", "system", "station"] = "region"
    """The location specification for the order summaries."""
    location_id: int
    """The location ID of the order summaries."""
    buy: MarketOrderSummaryDetails
    sell: MarketOrderSummaryDetails


class MarketOrderSummaries(TopLevelDataSet):
    """A collection model to make serialization faster."""

    location_spec: Literal["region", "system", "station"] = "region"
    """The location specification for the order summaries."""
    location_id: int
    """The location ID of the order summaries."""
    data: dict[int, MarketOrderSummary]
    """A dictionary mapping type IDs to market order summaries."""
