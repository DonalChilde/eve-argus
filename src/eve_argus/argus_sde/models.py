"""Pydantic models for data from the EVE Online FSD."""

from collections.abc import Sequence

from pydantic import BaseModel, Field


class FsdDataset(BaseModel):
    version: str


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
    probability: float | None = None


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


class Blueprints(FsdDataset):
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


class TypeInfos(FsdDataset):
    """A collection model to make serialization faster."""

    data: dict[int, TypeInfo] = {}


class TypeDescription(BaseModel):
    type_id: int
    description: str


class TypeDescriptions(FsdDataset):
    """A collection model to make serialization faster."""

    data: dict[int, TypeDescription] = {}


class MetaGroup(BaseModel):
    meta_id: int
    name: str


class MetaGroups(FsdDataset):
    """A collection model to make serialization faster."""

    data: dict[int, MetaGroup] = {}


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


class Groups(FsdDataset):
    data: dict[int, Group] = {}


class Category(BaseModel):
    category_id: int
    name: str
    published: bool


class Categories(FsdDataset):
    data: dict[int, Category] = {}


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
    path_ids: tuple[int, ...]
    """The path is a tuple of market group IDs leading to this group, including the current group."""
    parent_group_id: int | None


class MarketGroups(FsdDataset):
    """A collection model to make serialization faster."""

    data: dict[int, MarketGroup] = {}

    def path_string(self, group_ids: Sequence[int], separator: str = r"\\") -> str:
        """Create a string representation of the market group path."""
        return f"{separator}".join(
            str(self.data[group_id].name)
            for group_id in group_ids
            if group_id in self.data
        )
