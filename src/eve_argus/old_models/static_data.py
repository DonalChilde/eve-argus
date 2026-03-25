"""Models derived from data from the Eve Online SDE data.

Because these models are for internal use by eve-argus, they are different from the
TypedDict models in static_data_td.py. Notably, international string fields are
narrowed down to one language, represented as str, so that `name: LocalizedStringDict`
becomes `name: str`.

This is an incomplete set of models, added as needed.
As much as possible, match naming conventions from the sde models in static_data_td.py.
Note that pydantic treats fields with a leading underscore specially, so `_key` is not a valid field name.

Models are organized by SDE file. Each file-level model has a corresponding
from_td() classmethod to create an instance from the corresponding TypedDict from
static_data_td.py.

Sub-models are named with an underscore, e.g., Blueprint_Activities.

"""

import logging
from collections.abc import Iterable
from typing import Self, cast

from eve_static_data.models import static_data_td_3081406 as static_data_td
from eve_static_data.sde_access_protocol import SdeAccessProtocol, SdeFileNames
from pydantic import BaseModel, RootModel

from .helpers import BaseModelToDisk, RootModelToDisk

logger = logging.getLogger(__name__)


def localize_string_dict(
    string_dict: static_data_td.LocalizedStringDict | None, localized: str = "en"
) -> str:
    """Extract the localized string from a LocalizedStringDict.

    Args:
        string_dict: The LocalizedStringDict to extract from.
        localized: The language code to extract (default is "en" for English).

    Returns:
        The localized string.
    """
    if string_dict is None:
        return ""
    if localized not in string_dict:
        raise ValueError(f"Localized string for '{localized}' not found.")
    return string_dict.get(localized, "")


# ------------------------------------------------------------------------------
# Sub-level Pydantic model definitions.
# ------------------------------------------------------------------------------


class Position(BaseModel):
    x: float
    y: float
    z: float


# ------------------------------------------------------------------------------
# File level Pydantic model definitions.
# ------------------------------------------------------------------------------
class SdeInfo(BaseModelToDisk):
    """Model for SDE information."""

    key: str
    buildNumber: int
    releaseDate: str

    @classmethod
    def from_td(cls, td: static_data_td.SdeInfoDict) -> "SdeInfo":
        """Create an SdeInfo model from a static_data_td.SdeInfoDict TypedDict."""
        return cls(
            key=td["_key"],
            buildNumber=td["buildNumber"],
            releaseDate=td["releaseDate"],
        )

    @classmethod
    def from_sap(cls, access: SdeAccessProtocol) -> "SdeInfo":
        """Create an SdeInfo model from an SdeAccessProtocol."""
        info_td = next(iter(access.jsonl_iter(SdeFileNames.SDE_INFO)))
        info_td = cast(static_data_td.SdeInfoDict, info_td)
        return cls.from_td(info_td)


class Blueprint_Materials(BaseModel):
    """Model for material requirements in blueprints.jsonl."""

    typeID: int
    quantity: int

    @classmethod
    def from_td(cls, td: static_data_td.MaterialsDict) -> "Blueprint_Materials":
        """Create a Materials model from a static_data_td.MaterialsDict TypedDict."""
        return cls(
            typeID=td["typeID"],
            quantity=td["quantity"],
        )


class Blueprint_Skills(BaseModel):
    """Model for skill requirements in blueprints.jsonl."""

    typeID: int
    level: int

    @classmethod
    def from_td(cls, td: static_data_td.SkillsDict) -> "Blueprint_Skills":
        """Create a Skills model from a static_data_td.SkillsDict TypedDict."""
        return cls(
            typeID=td["typeID"],
            level=td["level"],
        )


class Blueprint_Products(BaseModel):
    """Model for products in blueprints.jsonl."""

    typeID: int
    quantity: int
    probability: float | None

    @classmethod
    def from_td(cls, td: static_data_td.ProductsDict) -> "Blueprint_Products":
        """Create a Products model from a static_data_td.ProductsDict TypedDict."""
        return cls(
            typeID=td["typeID"],
            quantity=td["quantity"],
            probability=td.get("probability"),
        )


class Blueprint_Activity(BaseModel):
    """Model for activities in blueprints.jsonl."""

    materials: list[Blueprint_Materials]
    skills: list[Blueprint_Skills]
    time: int
    products: list[Blueprint_Products] | None

    @classmethod
    def from_td(cls, td: static_data_td.ActivityDict) -> "Blueprint_Activity":
        """Create an Activity model from a static_data_td.ActivityDict TypedDict."""
        return cls(
            materials=[Blueprint_Materials.from_td(m) for m in td.get("materials", [])],
            products=[Blueprint_Products.from_td(p) for p in td["products"]]
            if "products" in td
            else None,
            skills=[Blueprint_Skills.from_td(s) for s in td.get("skills", [])],
            time=td["time"],
        )


class Blueprint_Activities(BaseModel):
    """Model for activities in blueprints.jsonl."""

    manufacturing: Blueprint_Activity | None
    research_material: Blueprint_Activity | None
    research_time: Blueprint_Activity | None
    copying: Blueprint_Activity | None
    invention: Blueprint_Activity | None

    @classmethod
    def from_td(cls, td: static_data_td.ActivitiesDict) -> "Blueprint_Activities":
        """Create an Activities model from a static_data_td.ActivitiesDict TypedDict."""
        return cls(
            manufacturing=Blueprint_Activity.from_td(td["manufacturing"])
            if "manufacturing" in td
            else None,
            research_material=Blueprint_Activity.from_td(td["researchMaterial"])
            if "researchMaterial" in td
            else None,
            research_time=Blueprint_Activity.from_td(td["researchTime"])
            if "researchTime" in td
            else None,
            copying=Blueprint_Activity.from_td(td["copying"])
            if "copying" in td
            else None,
            invention=Blueprint_Activity.from_td(td["invention"])
            if "invention" in td
            else None,
        )


class Blueprint(BaseModel):
    """Model for file blueprints.jsonl, as represented in static_data_td.BlueprintsDict."""

    key: int
    blueprintTypeID: int
    maxProductionLimit: int
    activities: Blueprint_Activities

    @classmethod
    def from_td(cls, td: static_data_td.BlueprintsDict) -> "Blueprint":
        """Create a Blueprint model from a static_data_td.BlueprintsDict TypedDict."""
        return cls(
            key=td["_key"],
            blueprintTypeID=td["blueprintTypeID"],
            maxProductionLimit=td["maxProductionLimit"],
            activities=Blueprint_Activities.from_td(td["activities"]),
        )


class Blueprints(BaseModelToDisk):
    info: SdeInfo
    source_name: str
    data: dict[int, Blueprint]

    @classmethod
    def from_static_data(
        cls,
        static_data: Iterable[static_data_td.BlueprintsDict],
        sde_info: SdeInfo,
        source_name: str,
        only_published: bool = False,
    ) -> "Blueprints":
        """Create a Blueprints model from an iterable of Blueprint models."""
        result = cls(data={}, info=sde_info, source_name=source_name)
        for bp in static_data:
            if only_published and not bp.get("published", True):
                continue
            result.data[bp["_key"]] = Blueprint.from_td(bp)
        return result

    @classmethod
    def from_sap(cls, access: SdeAccessProtocol, only_published: bool) -> "Blueprints":
        """Create a Blueprints model from an SdeAccessProtocol."""
        sde_info = SdeInfo.from_sap(access)
        blueprints_td = [
            cast(static_data_td.BlueprintsDict, bp_td)
            for bp_td in access.jsonl_iter(SdeFileNames.BLUEPRINTS)
        ]
        return cls.from_static_data(
            static_data=blueprints_td,
            sde_info=sde_info,
            source_name=SdeFileNames.BLUEPRINTS,
            only_published=only_published,
        )


class Category(BaseModel):
    """Model for file categories.jsonl, as represented in static_data_td.CategoriesDict."""

    key: int
    name: str
    published: bool
    icon_id: int | None

    @classmethod
    def from_td(
        cls, td: static_data_td.CategoriesDict, *, localized: str = "en"
    ) -> "Category":
        """Create a Category model from a static_data_td.CategoriesDict TypedDict."""
        return cls(
            key=td["_key"],
            name=localize_string_dict(td["name"], localized),
            published=td["published"],
            icon_id=td.get("icon_id"),
        )


class Categories(BaseModelToDisk):
    info: SdeInfo
    source_name: str
    data: dict[int, Category]

    @classmethod
    def from_static_data(
        cls,
        static_data: Iterable[static_data_td.CategoriesDict],
        localized: str,
        sde_info: SdeInfo,
        source_name: str,
        only_published: bool = False,
    ) -> "Categories":
        """Create a Categories model from an iterable of Category models."""
        result = cls(data={}, info=sde_info, source_name=source_name)
        for cat in static_data:
            if only_published and not cat.get("published", True):
                continue
            result.data[cat["_key"]] = Category.from_td(cat, localized=localized)
        return result

    @classmethod
    def from_sap(
        cls, access: SdeAccessProtocol, localized: str, only_published: bool
    ) -> "Categories":
        """Create a Categories model from an SdeAccessProtocol."""
        sde_info = SdeInfo.from_sap(access)
        categories_td = [
            cast(static_data_td.CategoriesDict, cat_td)
            for cat_td in access.jsonl_iter(SdeFileNames.CATEGORIES)
        ]
        return cls.from_static_data(
            static_data=categories_td,
            localized=localized,
            sde_info=sde_info,
            source_name=SdeFileNames.CATEGORIES,
            only_published=only_published,
        )


class Group(BaseModel):
    """Model for file groups.jsonl, as represented in static_data_td.GroupsDict."""

    key: int
    anchorable: bool
    anchored: bool
    categoryID: int
    fittableNonSingleton: bool
    name: str
    published: bool
    useBasePrice: bool
    iconID: int | None

    @classmethod
    def from_td(
        cls, td: static_data_td.GroupsDict, *, localized: str = "en"
    ) -> "Group":
        """Create a Group model from a static_data_td.GroupsDict TypedDict."""
        return cls(
            key=td["_key"],
            anchorable=td["anchorable"],
            anchored=td["anchored"],
            categoryID=td["categoryID"],
            fittableNonSingleton=td["fittableNonSingleton"],
            name=localize_string_dict(td["name"], localized),
            published=td["published"],
            useBasePrice=td["useBasePrice"],
            iconID=td.get("iconID"),
        )


class Groups(BaseModelToDisk):
    info: SdeInfo
    source_name: str
    data: dict[int, Group]

    @classmethod
    def from_static_data(
        cls,
        static_data: Iterable[static_data_td.GroupsDict],
        localized: str,
        sde_info: SdeInfo,
        source_name: str,
        only_published: bool = False,
    ) -> "Groups":
        """Create a Groups model from an iterable of Group models."""
        result = cls(data={}, info=sde_info, source_name=source_name)
        for group in static_data:
            if only_published and not group.get("published", True):
                continue
            result.data[group["_key"]] = Group.from_td(group, localized=localized)
        return result

    @classmethod
    def from_sap(
        cls, access: SdeAccessProtocol, localized: str, only_published: bool
    ) -> "Groups":
        """Create a Groups model from an SdeAccessProtocol."""
        sde_info = SdeInfo.from_sap(access)
        groups_td = [
            cast(static_data_td.GroupsDict, group_td)
            for group_td in access.jsonl_iter(SdeFileNames.GROUPS)
        ]
        return cls.from_static_data(
            static_data=groups_td,
            localized=localized,
            sde_info=sde_info,
            source_name=SdeFileNames.GROUPS,
            only_published=only_published,
        )


class MarketGroup(BaseModel):
    """Model for file marketGroups.jsonl, as represented in static_data_td.MarketGroupsDict."""

    key: int
    description: str
    hasTypes: bool
    iconID: int | None
    name: str
    parentGroupID: int | None

    @classmethod
    def from_td(
        cls, td: static_data_td.MarketGroupsDict, *, localized: str = "en"
    ) -> "MarketGroup":
        """Create a MarketGroup model from a static_data_td.MarketGroupsDict TypedDict."""
        return cls(
            key=td["_key"],
            name=localize_string_dict(td["name"], localized),
            description=localize_string_dict(td.get("description"), localized),
            hasTypes=td["hasTypes"],
            parentGroupID=td.get("parentGroupID"),
            iconID=td.get("iconID"),
        )


class MarketGroups(BaseModelToDisk):
    info: SdeInfo
    source_name: str
    data: dict[int, MarketGroup]
    market_path_ids: dict[int, list[int]]
    market_path_names: dict[int, str]

    @classmethod
    def from_static_data(
        cls,
        static_data: Iterable[static_data_td.MarketGroupsDict],
        localized: str,
        sde_info: SdeInfo,
        source_name: str,
    ) -> "MarketGroups":
        """Create a MarketGroups model from an iterable of MarketGroups models."""
        result = cls(
            data={},
            info=sde_info,
            source_name=source_name,
            market_path_ids={},
            market_path_names={},
        )
        for mg in static_data:
            result.data[mg["_key"]] = MarketGroup.from_td(mg, localized=localized)
        for mg_id in result.data:
            result.market_path_ids[mg_id] = get_market_path_int(mg_id, result.data)
            result.market_path_names[mg_id] = get_market_path_string(
                result.market_path_ids[mg_id], result.data
            )
        return result

    @classmethod
    def from_sap(cls, access: SdeAccessProtocol, localized: str) -> "MarketGroups":
        """Create a MarketGroups model from an SdeAccessProtocol."""
        sde_info = SdeInfo.from_sap(access)
        market_groups_td = [
            cast(static_data_td.MarketGroupsDict, mg_td)
            for mg_td in access.jsonl_iter(SdeFileNames.MARKET_GROUPS)
        ]
        return cls.from_static_data(
            static_data=market_groups_td,
            localized=localized,
            sde_info=sde_info,
            source_name=SdeFileNames.MARKET_GROUPS,
        )

    def get_market_path_ids(self, market_group_id: int) -> list[int]:
        """Get the market path as a list of integers for a given market group ID."""
        if market_group_id not in self._market_path_ids:
            raise ValueError(
                f"Market group ID {market_group_id} not found in market groups."
            )
        return self._market_path_ids[market_group_id]

    def get_market_path_names(self, market_group_id: int) -> str:
        """Get the market path as a string for a given market group ID."""
        if market_group_id not in self._market_path_names:
            raise ValueError(
                f"Market group ID {market_group_id} not found in market groups."
            )
        return self._market_path_names[market_group_id]


class MetaGroup(BaseModel):
    """Model for file metaGroups.jsonl, as represented in static_data_td.MetaGroupsDict."""

    key: int
    color: static_data_td.ColorDict | None
    name: str
    iconID: int | None
    iconSuffix: str | None
    description: str | None

    @classmethod
    def from_td(
        cls, td: static_data_td.MetaGroupsDict, *, localized: str = "en"
    ) -> "MetaGroup":
        """Create a MetaGroup model from a static_data_td.MetaGroupsDict TypedDict."""
        return cls(
            key=td["_key"],
            name=localize_string_dict(td["name"], localized),
            color=td.get("color"),
            iconID=td.get("iconID"),
            iconSuffix=td.get("iconSuffix"),
            description=localize_string_dict(td.get("description"), localized),
        )


class MetaGroups(BaseModelToDisk):
    info: SdeInfo
    source_name: str
    data: dict[int, MetaGroup]

    @classmethod
    def from_static_data(
        cls,
        static_data: Iterable[static_data_td.MetaGroupsDict],
        localized: str,
        sde_info: SdeInfo,
        source_name: str,
    ) -> "MetaGroups":
        """Create a MetaGroups model from an iterable of MetaGroup models."""
        result = cls(data={}, info=sde_info, source_name=source_name)
        for mg in static_data:
            result.data[mg["_key"]] = MetaGroup.from_td(mg, localized=localized)
        return result

    @classmethod
    def from_sap(cls, access: SdeAccessProtocol, localized: str) -> "MetaGroups":
        """Create a MetaGroups model from an SdeAccessProtocol."""
        sde_info = SdeInfo.from_sap(access)
        meta_groups_td = [
            cast(static_data_td.MetaGroupsDict, mg_td)
            for mg_td in access.jsonl_iter(SdeFileNames.META_GROUPS)
        ]
        return cls.from_static_data(
            static_data=meta_groups_td,
            localized=localized,
            sde_info=sde_info,
            source_name=SdeFileNames.META_GROUPS,
        )


class TypeMaterials_Materials(BaseModel):
    """Model for material requirements in typeMaterials.jsonl."""

    materialTypeID: int
    quantity: int

    @classmethod
    def from_td(
        cls, td: static_data_td.MaterialsMateritalsDict
    ) -> "TypeMaterials_Materials":
        """Create a Materials model from a static_data_td.MaterialsMaterialsDict TypedDict."""
        return cls(
            materialTypeID=td["materialTypeID"],
            quantity=td["quantity"],
        )


class TypeMaterials_RandomizedMaterials(BaseModel):
    """Model for random material requirements in typeMaterials.jsonl.

    {"_key": 90041, "randomizedMaterials": [{"materialTypeID": 34, "quantityMax": 496800, "quantityMin": 368000},]}
    """

    materialTypeID: int
    quantityMax: int
    quantityMin: int

    @classmethod
    def from_td(cls, td: dict[str, int]) -> Self:
        """Create a RandomMaterials model from a static_data_td.MaterialsRandomMaterialsDict TypedDict."""
        return cls(
            materialTypeID=td["materialTypeID"],
            quantityMax=td["quantityMax"],
            quantityMin=td["quantityMin"],
        )


class TypeMaterial(BaseModel):
    """Model for file typeMaterials.jsonl, as represented in static_data_td.TypeMaterialsDict."""

    key: int
    materials: list[TypeMaterials_Materials] | None = None
    randomized_materials: list[TypeMaterials_RandomizedMaterials] | None = None

    @classmethod
    def from_td(cls, td: static_data_td.TypeMaterialsDict) -> "TypeMaterial":
        """Create a TypeMaterials model from a static_data_td.TypeMaterialsDict TypedDict."""
        materials_td = td.get("materials")
        randomized_materials_td = td.get("randomizedMaterials")
        if materials_td and randomized_materials_td:
            return cls(
                key=td["_key"],
                materials=[TypeMaterials_Materials.from_td(m) for m in materials_td],
                randomized_materials=[
                    TypeMaterials_RandomizedMaterials.from_td(m)
                    for m in randomized_materials_td
                ],
            )
        if materials_td:
            return cls(
                key=td["_key"],
                materials=[TypeMaterials_Materials.from_td(m) for m in materials_td],
            )
        if randomized_materials_td:
            return cls(
                key=td["_key"],
                randomized_materials=[
                    TypeMaterials_RandomizedMaterials.from_td(m)
                    for m in randomized_materials_td
                ],
            )
        raise ValueError(
            f"TypeMaterial with _key {td['_key']} has neither materials nor randomizedMaterials."
        )


class TypeMaterials(BaseModelToDisk):
    info: SdeInfo
    source_name: str
    data: dict[int, TypeMaterial]

    @classmethod
    def from_static_data(
        cls,
        static_data: Iterable[static_data_td.TypeMaterialsDict],
        sde_info: SdeInfo,
        source_name: str,
    ) -> "TypeMaterials":
        """Create a TypeMaterials model from an iterable of TypeMaterial models."""
        result = cls(data={}, info=sde_info, source_name=source_name)
        for tm in static_data:
            result.data[tm["_key"]] = TypeMaterial.from_td(tm)
        return result

    @classmethod
    def from_sap(cls, access: SdeAccessProtocol) -> "TypeMaterials":
        """Create a TypeMaterials model from an SdeAccessProtocol."""
        sde_info = SdeInfo.from_sap(access)
        type_materials_td = [
            cast(static_data_td.TypeMaterialsDict, tm_td)
            for tm_td in access.jsonl_iter(SdeFileNames.TYPE_MATERIALS)
        ]
        return cls.from_static_data(
            static_data=type_materials_td,
            sde_info=sde_info,
            source_name=SdeFileNames.TYPE_MATERIALS,
        )


class EveType(BaseModel):
    """Model for file types.jsonl, as represented in static_data_td.TypesDict."""

    key: int
    groupID: int
    mass: float | None
    name: str
    portionSize: int
    published: bool
    volume: float | None
    radius: float | None
    description: str | None
    graphicID: int | None
    soundID: int | None
    iconID: int | None
    raceID: int | None
    basePrice: float | None
    marketGroupID: int | None
    capacity: float | None
    metaGroupID: int | None
    variationParentTypeID: int | None
    factionID: int | None

    @classmethod
    def from_td(
        cls, td: static_data_td.TypesDict, *, localized: str = "en"
    ) -> "EveType":
        """Create a Types model from a static_data_td.TypesDict TypedDict."""
        return cls(
            key=td["_key"],
            groupID=td["groupID"],
            name=localize_string_dict(td["name"], localized),
            description=localize_string_dict(td.get("description"), localized),
            mass=td.get("mass"),
            volume=td.get("volume"),
            capacity=td.get("capacity"),
            portionSize=td.get("portionSize", 1),
            published=td.get("published", False),
            radius=td.get("radius"),
            graphicID=td.get("graphicID"),
            soundID=td.get("soundID"),
            iconID=td.get("iconID"),
            raceID=td.get("raceID"),
            basePrice=td.get("basePrice"),
            marketGroupID=td.get("marketGroupID"),
            metaGroupID=td.get("metaGroupID"),
            variationParentTypeID=td.get("variationParentTypeID"),
            factionID=td.get("factionID"),
        )


class EveTypes(BaseModelToDisk):
    info: SdeInfo
    source_name: str
    data: dict[int, EveType]

    @classmethod
    def from_static_data(
        cls,
        static_data: Iterable[static_data_td.TypesDict],
        localized: str,
        only_published: bool,
        sde_info: SdeInfo,
        source_name: str,
    ) -> "EveTypes":
        """Create an EveTypes model from an iterable of EveType models."""
        result = cls(data={}, info=sde_info, source_name=source_name)
        for et in static_data:
            if only_published and not et.get("published", True):
                continue
            result.data[et["_key"]] = EveType.from_td(et, localized=localized)
        return result

    @classmethod
    def from_sap(
        cls, access: SdeAccessProtocol, localized: str, only_published: bool
    ) -> "EveTypes":
        """Create an EveTypes model from an SdeAccessProtocol."""
        sde_info = SdeInfo.from_sap(access)
        types_td = [
            cast(static_data_td.TypesDict, type_td)
            for type_td in access.jsonl_iter(SdeFileNames.TYPES)
        ]
        return cls.from_static_data(
            static_data=types_td,
            localized=localized,
            only_published=only_published,
            sde_info=sde_info,
            source_name=SdeFileNames.TYPES,
        )


class Region(BaseModel):
    key: int
    name: str
    constellationIDs: list[int]
    description: str | None
    factionID: int | None
    nebulaID: int
    position: Position
    wormholeClassID: int | None

    @classmethod
    def from_td(
        cls, td: static_data_td.MapRegionsDict, *, localized: str = "en"
    ) -> "Region":
        """Create a Region model from a static_data_td.RegionsDict TypedDict."""
        position_td = td["position"]
        return cls(
            key=td["_key"],
            name=localize_string_dict(td["name"], localized),
            constellationIDs=list(td["constellationIDs"]),
            description=localize_string_dict(td.get("description"), localized),
            factionID=td.get("factionID"),
            nebulaID=td["nebulaID"],
            position=Position(
                x=position_td["x"],
                y=position_td["y"],
                z=position_td["z"],
            ),
            wormholeClassID=td.get("wormholeClassID"),
        )


class Regions(BaseModelToDisk):
    info: SdeInfo
    source_name: str
    data: dict[int, Region]

    @classmethod
    def from_static_data(
        cls,
        static_data: Iterable[static_data_td.MapRegionsDict],
        sde_info: SdeInfo,
        source_name: str,
        localized: str = "en",
    ) -> "Regions":
        """Create a Regions model from an iterable of Regions models."""
        result = cls(data={}, info=sde_info, source_name=source_name)
        for region in static_data:
            result.data[region["_key"]] = Region.from_td(region, localized=localized)
        return result

    @classmethod
    def from_sap(cls, access: SdeAccessProtocol, localized: str) -> "Regions":
        """Create a Regions model from an SdeAccessProtocol."""
        sde_info = SdeInfo.from_sap(access)
        regions_td = [
            cast(static_data_td.MapRegionsDict, region_td)
            for region_td in access.jsonl_iter(SdeFileNames.MAP_REGIONS)
        ]
        return cls.from_static_data(
            static_data=regions_td,
            sde_info=sde_info,
            source_name=SdeFileNames.MAP_REGIONS,
        )


# --------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------


class ArgusStaticData(BaseModelToDisk):
    """Model for all static data used by Eve Argus."""

    sde_info: SdeInfo
    blueprints: dict[int, Blueprint]
    categories: dict[int, Category]
    groups: dict[int, Group]
    market_groups: dict[int, MarketGroup]
    meta_groups: dict[int, MetaGroup]
    type_materials: dict[int, TypeMaterial]
    eve_types: dict[int, EveType]


def get_market_path_int(
    market_group_id: int, market_groups: dict[int, MarketGroup]
) -> list[int]:
    """Get the market path as a list of integers for a given market group ID.

    Starting from the given market group ID, traverse up the parentGroupIDs
    to build the full path to the root market group. Path is returned as a list
    of integers representing market group IDs from root to the specified market group.
    """
    if market_group_id not in market_groups:
        raise ValueError(
            f"Market group ID {market_group_id} not found in market groups."
        )

    def get_path(market_group_id: int) -> list[int]:
        path: list[int] = []
        current = market_groups.get(market_group_id)
        while current:
            path.append(current.key)
            if current.parentGroupID is None:
                break
            current = market_groups.get(current.parentGroupID)
        return path

    path = get_path(market_group_id)
    if not path:
        raise ValueError(
            f"Market group ID {market_group_id} not found in market groups."
        )
    return list(reversed(path))


def get_market_path_string(
    market_path: list[int],
    market_groups: dict[int, MarketGroup],
    separator: str = "/",
) -> str:
    """Get the market path as a string for a given market path list of integers."""
    names: list[str] = []
    for mg_id in market_path:
        market_group = market_groups.get(mg_id)
        if market_group is None:
            raise ValueError(f"Market group ID {mg_id} not found in market groups.")
        names.append(market_group.name)
    return separator.join(names)
