"""Static data models for Eve Online SDE data.

Because these models are for internal use by eve-argus, they are different from the
TypedDict models in static_data_td.py. Notably, international string fields are
narrowed down to one language, represented as str, so that `name: LocalizedStringDict`
becomes `name: str`.

This is an incomplete set of models, added as needed.
As much as possible, match naming conventions from the sde models in static_data_td.py.
"""

from pydantic import BaseModel

from ..models import static_data_td

_ = static_data_td  # Ensure TypedDicts are imported


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


class Category(BaseModel):
    """Model for file categories.jsonl, as represented in static_data_td.CategoriesDict."""

    _key: int
    name: str
    published: bool
    icon_id: int | None

    @classmethod
    def from_td(
        cls, td: static_data_td.CategoriesDict, localized: str = "en"
    ) -> "Category":
        """Create a Category model from a static_data_td.CategoriesDict TypedDict."""
        return cls(
            _key=td["_key"],
            name=localize_string_dict(td["name"], localized),
            published=td["published"],
            icon_id=td.get("icon_id"),
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
    def from_td(cls, td: static_data_td.GroupsDict, localized: str = "en") -> "Group":
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
        cls, td: static_data_td.MarketGroupsDict, localized: str = "en"
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
        cls, td: static_data_td.MetaGroupsDict, localized: str = "en"
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


class SdeInfo(BaseModel):
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


class TypeMaterials(BaseModel):
    """Model for file typeMaterials.jsonl, as represented in static_data_td.TypeMaterialsDict."""

    _key: int
    materials: list[MaterialsMaterials]

    @classmethod
    def from_td(cls, td: static_data_td.TypeMaterialsDict) -> "TypeMaterials":
        """Create a TypeMaterials model from a static_data_td.TypeMaterialsDict TypedDict."""
        return cls(
            _key=td["_key"],
            materials=[MaterialsMaterials.from_td(m) for m in td["materials"]],
        )


class Types(BaseModel):
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
    def from_td(cls, td: static_data_td.TypesDict, localized: str = "en") -> "Types":
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


class ArgusStaticData(BaseModel):
    """Model for all static data used by Eve Argus."""

    sde_info: SdeInfo
    blueprints: dict[int, Blueprint]
    categories: dict[int, Category]
    groups: dict[int, Group]
    market_groups: dict[int, MarketGroup]
    meta_groups: dict[int, MetaGroup]
    type_materials: dict[int, TypeMaterials]
    types: dict[int, Types]
