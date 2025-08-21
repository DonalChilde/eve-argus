"""FSD schema definitions as TypedDicts."""

from collections.abc import Sequence
from typing import NotRequired, TypedDict


class FSDLocalizedTD(TypedDict):
    de: str
    en: str
    es: str
    fr: str
    ja: str
    ko: str
    ru: str
    zh: str


class CategoryTD(TypedDict):
    name: FSDLocalizedTD
    published: bool
    iconID: NotRequired[int]


Categories = dict[int, CategoryTD]
"""Indexed by category_id."""


class MetaGroupTD(TypedDict):
    nameID: FSDLocalizedTD
    published: bool
    color: Sequence[float]
    iconID: int
    iconSuffix: str
    descriptionID: FSDLocalizedTD


MetaGroups = dict[int, MetaGroupTD]
"""Indexed by meta_id."""


class GroupTD(TypedDict):
    anchorable: bool
    anchored: bool
    categoryID: int
    fittableNonSingleton: bool
    iconID: NotRequired[int]
    name: FSDLocalizedTD
    published: bool
    useBasePrice: bool


Groups = dict[int, GroupTD]
"""Indexed by group_id."""


class MarketGroupTD(TypedDict):
    parentGroupID: NotRequired[int]
    name: FSDLocalizedTD
    description: FSDLocalizedTD
    iconID: NotRequired[int]
    hasTypes: bool


MarketGroups = dict[int, MarketGroupTD]
"""Indexed by marketGroupID."""


class MaterialsTD(TypedDict):
    typeID: int
    quantity: int


class SkillsTD(TypedDict):
    typeID: int
    level: int


class BlueprintActivityTD(TypedDict):
    time: int
    materials: NotRequired[list[MaterialsTD]]
    products: NotRequired[list[MaterialsTD]]
    skills: NotRequired[list[SkillsTD]]
    probability: NotRequired[float]


class BlueprintActivitiesTD(TypedDict):
    manufacturing: NotRequired[BlueprintActivityTD]
    research_time: NotRequired[BlueprintActivityTD]
    research_material: NotRequired[BlueprintActivityTD]
    copying: NotRequired[BlueprintActivityTD]
    invention: NotRequired[BlueprintActivityTD]
    reaction: NotRequired[BlueprintActivityTD]


class BlueprintTD(TypedDict, total=False):
    blueprintTypeID: int
    activities: BlueprintActivitiesTD
    maxProductionLimit: int


Blueprints = dict[int, BlueprintTD]
"""Indexed by blueprintTypeID."""


class TypeInfoTD(TypedDict):
    basePrice: NotRequired[float]
    capacity: NotRequired[float]
    description: NotRequired[FSDLocalizedTD]
    graphicID: NotRequired[int]
    groupID: NotRequired[int]
    iconID: NotRequired[int]
    marketGroupID: NotRequired[int]
    mass: NotRequired[float]
    metaGroupID: NotRequired[int]
    name: FSDLocalizedTD
    portionSize: NotRequired[int]
    published: bool
    raceID: NotRequired[int]
    radius: NotRequired[float]
    sofFactionName: NotRequired[str]
    variationParentTypeID: NotRequired[int]
    volume: NotRequired[float]


TypeInfos = dict[int, TypeInfoTD]
"""Indexed by type_id."""
