"""Models for the Eve Argus app."""

from enum import Enum
from pydantic import BaseModel


class MarketHistory(BaseModel):
    """Market history data model."""

    date: str
    highest: float
    average: float
    lowest: float
    order_count: float
    volume: int


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


class Activity_Name(Enum):
    manufacturing = 1
    research_time = 3
    research_material = 4
    copying = 5
    invention = 8
    reaction = 11


class Material(BaseModel):
    quantity: int
    typeID: int


class Skill(BaseModel):
    level: int
    typeID: int


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


class BlueprintsDict(BaseModel):
    """A collection model to make serialization faster."""

    data: dict[int, Blueprint]


class TypeInfo(BaseModel):
    name: str
    typeID: int
    groupID: int | None
    marketGroupID: int | None
    metaGroupID: int | None
    graphicID: int | None
    capacity: float | None
    portionSize: int | None
    published: bool


class TypeInfoDict(BaseModel):
    """A collection model to make serialization faster."""

    data: dict[int, TypeInfo]


class TypeDescription(BaseModel):
    typeID: int
    description: str


class TypeDescriptionDict(BaseModel):
    """A collection model to make serialization faster."""

    data: dict[int, TypeDescription]


class MetaGroup(BaseModel):
    metaID: int
    name: str


class MetaGroupDict(BaseModel):
    """A collection model to make serialization faster."""

    data: dict[int, MetaGroup]


class Group(BaseModel):
    groupID: int
    anchorable: bool
    anchored: bool
    categoryID: int
    fittableNonSingleton: bool
    iconID: int  # -1 if no value in sde
    name: str
    published: bool
    useBasePrice: bool


class GroupDict(BaseModel):
    data: dict[int, Group]


class Category(BaseModel):
    categoryID: int
    name: str
    published: bool


class CategoryDict(BaseModel):
    data: dict[int, Category]


class MarketGroup(BaseModel):
    groupID: int
    name: str
    description: str
    hasTypes: bool
    iconID: int  # -1 if no value in sde
    path: tuple[int, ...]


class MarketGroupDict(BaseModel):
    """A collection model to make serialization faster."""

    data: dict[int, MarketGroup]
