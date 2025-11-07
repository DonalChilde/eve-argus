"""Collect static data from the SDE."""

from typing import cast

from eve_argus.models import static_data as SD
from eve_argus.models import static_data_td as SDTD
from eve_argus.sde.raw_jsonl_access import RawJsonAccess, SdeFileNames


def collect_blueprints(access: RawJsonAccess) -> dict[int, SD.Blueprint]:
    """Collect all blueprints from the static data.

    Returns:
        dict[int, Blueprint]: A dictionary mapping blueprint type IDs to Blueprint objects.
    """
    blueprints: dict[int, SD.Blueprint] = {}
    for blueprint_td in access.jsonl_iter(SdeFileNames.BLUEPRINTS):
        blueprint_td = cast(SDTD.BlueprintsDict, blueprint_td)
        blueprint = SD.Blueprint.from_td(blueprint_td)
        blueprints[blueprint._key] = blueprint
    return blueprints


def collect_categories(
    access: RawJsonAccess, *, language: str, only_published: bool
) -> dict[int, SD.Category]:
    """Collect all categories from the static data.

    Returns:
        dict[int, Category]: A dictionary mapping category IDs to Category objects.
    """
    categories: dict[int, SD.Category] = {}
    for category_td in access.jsonl_iter(SdeFileNames.CATEGORIES):
        category_td = cast(SDTD.CategoriesDict, category_td)
        if only_published and not category_td.get("published", True):
            continue
        category = SD.Category.from_td(category_td)
        categories[category._key] = category
    return categories


def collect_groups(
    access: RawJsonAccess, *, language: str, only_published: bool
) -> dict[int, SD.Group]:
    """Collect all groups from the static data.

    Returns:
        dict[int, Group]: A dictionary mapping group IDs to Group objects.
    """
    groups: dict[int, SD.Group] = {}
    for group_td in access.jsonl_iter(SdeFileNames.GROUPS):
        group_td = cast(SDTD.GroupsDict, group_td)
        if only_published and not group_td.get("published", True):
            continue
        group = SD.Group.from_td(group_td)
        groups[group._key] = group
    return groups


def collect_market_groups(
    access: RawJsonAccess, *, language: str
) -> dict[int, SD.MarketGroup]:
    """Collect all market groups from the static data.

    Returns:
        dict[int, MarketGroup]: A dictionary mapping market group IDs to MarketGroup objects.
    """
    market_groups: dict[int, SD.MarketGroup] = {}
    for market_group_td in access.jsonl_iter(SdeFileNames.MARKET_GROUPS):
        market_group_td = cast(SDTD.MarketGroupsDict, market_group_td)
        market_group = SD.MarketGroup.from_td(market_group_td)
        market_groups[market_group._key] = market_group
    return market_groups


def collect_meta_groups(
    access: RawJsonAccess, *, language: str
) -> dict[int, SD.MetaGroup]:
    """Collect all meta groups from the static data.

    Returns:
        dict[int, MetaGroup]: A dictionary mapping meta group IDs to MetaGroup objects.
    """
    meta_groups: dict[int, SD.MetaGroup] = {}
    for meta_group_td in access.jsonl_iter(SdeFileNames.META_GROUPS):
        meta_group_td = cast(SDTD.MetaGroupsDict, meta_group_td)
        meta_group = SD.MetaGroup.from_td(meta_group_td)
        meta_groups[meta_group._key] = meta_group
    return meta_groups


def collect_sde_info(access: RawJsonAccess) -> SD.SdeInfo:
    """Collect the SDE info from the static data.

    Returns:
        SdeInfo: The SdeInfo object.
    """
    info_td = next(iter(access.jsonl_iter(SdeFileNames.SDE_INFO)))
    info_td = cast(SDTD.SdeInfoDict, info_td)
    sde_info = SD.SdeInfo.from_td(info_td)
    return sde_info


def collect_type_materials(access: RawJsonAccess) -> dict[int, SD.TypeMaterials]:
    """Collect all type materials from the static data.

    Returns:
        dict[int, TypeMaterials]: A dictionary mapping type IDs to TypeMaterials objects.
    """
    type_materials: dict[int, SD.TypeMaterials] = {}
    for type_materials_td in access.jsonl_iter(SdeFileNames.TYPE_MATERIALS):
        type_materials_td = cast(SDTD.TypeMaterialsDict, type_materials_td)
        type_materials_obj = SD.TypeMaterials.from_td(type_materials_td)
        type_materials[type_materials_obj._key] = type_materials_obj
    return type_materials


def collect_types(
    access: RawJsonAccess, *, language: str, only_published: bool
) -> dict[int, SD.Types]:
    """Collect all types from the static data.

    Returns:
        dict[int, Types]: A dictionary mapping type IDs to Types objects.
    """
    types: dict[int, SD.Types] = {}
    for type_td in access.jsonl_iter(SdeFileNames.TYPES):
        type_td = cast(SDTD.TypesDict, type_td)
        if only_published and not type_td.get("published", True):
            continue
        type_obj = SD.Types.from_td(type_td)
        types[type_obj._key] = type_obj
    return types


def collect_argus_static_data(
    access: RawJsonAccess, *, language: str = "en", only_published: bool = True
) -> SD.ArgusStaticData:
    """Collect all static data used by Eve Argus.

    Returns:
        ArgusStaticData: The collected static data.
    """
    blueprints = collect_blueprints(access)
    categories = collect_categories(
        access, language=language, only_published=only_published
    )
    groups = collect_groups(access, language=language, only_published=only_published)
    market_groups = collect_market_groups(access, language=language)
    meta_groups = collect_meta_groups(access, language=language)
    sde_info = collect_sde_info(access)
    type_materials = collect_type_materials(access)
    types = collect_types(access, language=language, only_published=only_published)

    static_data = SD.ArgusStaticData(
        blueprints=blueprints,
        categories=categories,
        groups=groups,
        market_groups=market_groups,
        meta_groups=meta_groups,
        sde_info=sde_info,
        type_materials=type_materials,
        types=types,
    )
    return static_data
