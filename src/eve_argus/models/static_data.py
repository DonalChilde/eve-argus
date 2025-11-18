"""Models derived from data from the Eve Online SDE data.

Because these models are for internal use by eve-argus, they are different from the
TypedDict models in static_data_td.py. Notably, international string fields are
narrowed down to one language, represented as str, so that `name: LocalizedStringDict`
becomes `name: str`.

This is an incomplete set of models, added as needed.
As much as possible, match naming conventions from the sde models in static_data_td.py.
"""

import logging
from collections.abc import Iterable
from typing import cast

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


class MaterialsMaterials(BaseModel):
    """Model for material requirements in typeMaterials.jsonl."""

    materialTypeID: int
    quantity: int

    @classmethod
    def from_td(
        cls, td: static_data_td.MaterialsMateritalsDict
    ) -> "MaterialsMaterials":
        """Create a Materials model from a static_data_td.MaterialsMaterialsDict TypedDict."""
        return cls(
            materialTypeID=td["materialTypeID"],
            quantity=td["quantity"],
        )


class Materials(BaseModel):
    """Model for material requirements in blueprints.jsonl."""

    typeID: int
    quantity: int

    @classmethod
    def from_td(cls, td: static_data_td.MaterialsDict) -> "Materials":
        """Create a Materials model from a static_data_td.MaterialsDict TypedDict."""
        return cls(
            typeID=td["typeID"],
            quantity=td["quantity"],
        )


class Skills(BaseModel):
    """Model for skill requirements in blueprints.jsonl."""

    typeID: int
    level: int

    @classmethod
    def from_td(cls, td: static_data_td.SkillsDict) -> "Skills":
        """Create a Skills model from a static_data_td.SkillsDict TypedDict."""
        return cls(
            typeID=td["typeID"],
            level=td["level"],
        )


class Products(BaseModel):
    """Model for products in blueprints.jsonl."""

    typeID: int
    quantity: int
    probability: float | None

    @classmethod
    def from_td(cls, td: static_data_td.ProductsDict) -> "Products":
        """Create a Products model from a static_data_td.ProductsDict TypedDict."""
        return cls(
            typeID=td["typeID"],
            quantity=td["quantity"],
            probability=td.get("probability"),
        )


class Activity(BaseModel):
    """Model for activities in blueprints.jsonl."""

    materials: list[Materials]
    skills: list[Skills]
    time: int
    products: list[Products] | None

    @classmethod
    def from_td(cls, td: static_data_td.ActivityDict) -> "Activity":
        """Create an Activity model from a static_data_td.ActivityDict TypedDict."""
        return cls(
            materials=[Materials.from_td(m) for m in td["materials"]],
            products=[Products.from_td(p) for p in td["products"]]
            if "products" in td
            else None,
            skills=[Skills.from_td(s) for s in td["skills"]],
            time=td["time"],
        )


class Activities(BaseModel):
    """Model for activities in blueprints.jsonl."""

    manufacturing: Activity | None
    research_material: Activity | None
    research_time: Activity | None
    copying: Activity | None
    invention: Activity | None

    @classmethod
    def from_td(cls, td: static_data_td.ActivitiesDict) -> "Activities":
        """Create an Activities model from a static_data_td.ActivitiesDict TypedDict."""
        return cls(
            manufacturing=Activity.from_td(td["manufacturing"])
            if "manufacturing" in td
            else None,
            research_material=Activity.from_td(td["researchMaterial"])
            if "researchMaterial" in td
            else None,
            research_time=Activity.from_td(td["researchTime"])
            if "researchTime" in td
            else None,
            copying=Activity.from_td(td["copying"]) if "copying" in td else None,
            invention=Activity.from_td(td["invention"]) if "invention" in td else None,
        )


# ------------------------------------------------------------------------------
# File level Pydantic model definitions.
# ------------------------------------------------------------------------------
class SdeInfo(BaseModelToDisk):
    """Model for SDE information."""

    _key: str
    buildNumber: int
    releaseDate: str

    @classmethod
    def from_td(cls, td: static_data_td.SdeInfoDict) -> "SdeInfo":
        """Create an SdeInfo model from a static_data_td.SdeInfoDict TypedDict."""
        return cls(
            _key=td["_key"],
            buildNumber=td["buildNumber"],
            releaseDate=td["releaseDate"],
        )

    @classmethod
    def from_sap(cls, access: SdeAccessProtocol) -> "SdeInfo":
        """Create an SdeInfo model from an SdeAccessProtocol."""
        info_td = next(iter(access.jsonl_iter(SdeFileNames.SDE_INFO)))
        info_td = cast(static_data_td.SdeInfoDict, info_td)
        return cls.from_td(info_td)


class Blueprint(BaseModel):
    """Model for file blueprints.jsonl, as represented in static_data_td.BlueprintsDict."""

    _key: int
    blueprintTypeID: int
    maxProductionLimit: int
    activities: Activities

    @classmethod
    def from_td(cls, td: static_data_td.BlueprintsDict) -> "Blueprint":
        """Create a Blueprint model from a static_data_td.BlueprintsDict TypedDict."""
        return cls(
            _key=td["_key"],
            blueprintTypeID=td["blueprintTypeID"],
            maxProductionLimit=td["maxProductionLimit"],
            activities=Activities.from_td(td["activities"]),
        )


class Blueprints(BaseModelToDisk):
    data: dict[int, Blueprint]
    info: SdeInfo
    source_name: str

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

    _key: int
    name: str
    published: bool
    icon_id: int | None

    @classmethod
    def from_td(
        cls, td: static_data_td.CategoriesDict, *, localized: str = "en"
    ) -> "Category":
        """Create a Category model from a static_data_td.CategoriesDict TypedDict."""
        return cls(
            _key=td["_key"],
            name=localize_string_dict(td["name"], localized),
            published=td["published"],
            icon_id=td.get("icon_id"),
        )


class Categories(BaseModelToDisk):
    data: dict[int, Category]
    info: SdeInfo
    source_name: str

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

    _key: int
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
            _key=td["_key"],
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
    data: dict[int, Group]
    info: SdeInfo
    source_name: str

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

    _key: int
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
            _key=td["_key"],
            name=localize_string_dict(td["name"], localized),
            description=localize_string_dict(td.get("description"), localized),
            hasTypes=td["hasTypes"],
            parentGroupID=td.get("parentGroupID"),
            iconID=td.get("iconID"),
        )


class MarketGroups(BaseModelToDisk):
    data: dict[int, MarketGroup]
    info: SdeInfo
    source_name: str
    _market_path_ids: dict[int, list[int]]
    _market_path_names: dict[int, str]

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
            _market_path_ids={},
            _market_path_names={},
        )
        for mg in static_data:
            result.data[mg["_key"]] = MarketGroup.from_td(mg, localized=localized)
        for mg_id in result.data:
            result._market_path_ids[mg_id] = get_market_path_int(mg_id, result.data)
            result._market_path_names[mg_id] = get_market_path_string(
                result._market_path_ids[mg_id], result.data
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

    _key: int
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
            _key=td["_key"],
            name=localize_string_dict(td["name"], localized),
            color=td.get("color"),
            iconID=td.get("iconID"),
            iconSuffix=td.get("iconSuffix"),
            description=localize_string_dict(td.get("description"), localized),
        )


class MetaGroups(BaseModelToDisk):
    data: dict[int, MetaGroup]
    info: SdeInfo
    source_name: str

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


class TypeMaterial(BaseModel):
    """Model for file typeMaterials.jsonl, as represented in static_data_td.TypeMaterialsDict."""

    _key: int
    materials: list[MaterialsMaterials]

    @classmethod
    def from_td(cls, td: static_data_td.TypeMaterialsDict) -> "TypeMaterial":
        """Create a TypeMaterials model from a static_data_td.TypeMaterialsDict TypedDict."""
        return cls(
            _key=td["_key"],
            materials=[MaterialsMaterials.from_td(m) for m in td["materials"]],
        )


class TypeMaterials(BaseModelToDisk):
    data: dict[int, TypeMaterial]
    info: SdeInfo
    source_name: str

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

    _key: int
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
            _key=td["_key"],
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
    data: dict[int, EveType]
    info: SdeInfo
    source_name: str

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
        path = []
        current = market_groups.get(market_group_id)
        while current:
            path.append(current._key)
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
    names = []
    for mg_id in market_path:
        market_group = market_groups.get(mg_id)
        if market_group is None:
            raise ValueError(f"Market group ID {mg_id} not found in market groups.")
        names.append(market_group.name)
    return separator.join(names)
