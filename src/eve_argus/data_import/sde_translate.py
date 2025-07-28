"""Functions for using the Eve SDE."""

from collections.abc import Sequence
from typing import Any

from eve_argus.models import argus as EAM


def sde_types(
    sde_types: dict[int, dict[str, Any]],
    skip_unpublished: bool = True,
    lang: str = "en",
) -> tuple[EAM.TypeInfos, EAM.TypeDescriptions]:
    """Import TypeInfo from sde, with an optional filter of unpublished items.

    Split off the description data, and keep only one language. Only keeps fields used
    by Eve Argus

    Args:
        sde_types (dict[int, dict[str, Any]]): _description_
        skip_unpublished (bool, optional): _description_. Defaults to True.
        lang (str, optional): _description_. Defaults to "en".

    Returns:
        tuple[EAM.TypeInfos, EAM.TypeDescriptions]: Tuple containing TypeInfos and TypeDescriptions.
    """
    argus_types = EAM.TypeInfos(data={})
    argus_descriptions = EAM.TypeDescriptions(data={})
    # Iterate over the SDE types and filter based on the skip_unpublished flag
    # and the specified language.
    for key, value in sde_types.items():
        if skip_unpublished:
            if value.get("published", False) == False:
                continue
        try:
            name = value["name"][lang]
        except KeyError:
            name = ""
        try:
            description = value["description"][lang]
        except KeyError:
            description = ""
        argus_types.data[key] = EAM.TypeInfo(
            name=name,
            type_id=key,
            group_id=value.get("groupID", None),
            market_group_id=value.get("marketGroupID", None),
            meta_group_id=value.get("metaGroupID", None),
            graphic_id=value.get("graphicID", None),
            capacity=value.get("capacity", None),
            portion_size=value.get("portionSize", -1),
            published=value.get("published", False),
        )

        argus_descriptions.data[key] = EAM.TypeDescription(
            type_id=key, description=description
        )
    # Return the TypeInfos and TypeDescriptions as a tuple
    return (argus_types, argus_descriptions)


def blueprints(
    sde_blueprints: dict[int, dict[str, Any]],
) -> EAM.Blueprints:
    """Import blueprints from the SDE.

    Args:
        sde_blueprints (dict[int, dict[str, Any]]): Dictionary of blueprint data from SDE.

    Returns:
        EAM.Blueprints: Collection of validated Blueprint models.
    """
    blueprints = EAM.Blueprints(data={})
    for sde_item in sde_blueprints.values():
        bp = EAM.Blueprint.model_validate(sde_item)
        blueprints.data[bp.blueprintTypeID] = bp
    return blueprints


def market_groups(
    sde_market_groups: dict[int, dict[str, Any]], lang: str = "en"
) -> EAM.MarketGroups:
    """Import market groups from the SDE.

    Args:
        sde_market_groups (dict[int, dict[str, Any]]): Dictionary of market group data from SDE.
        lang (str, optional): Language code for names and descriptions. Defaults to "en".

    Returns:
        EAM.MarketGroups: Collection of validated MarketGroup models.
    """
    market_groups = EAM.MarketGroups(data={})
    for key, value in sde_market_groups.items():
        path_id = key
        parent_path: Sequence[int] = []
        current = sde_market_groups[path_id]
        while True:
            if path_id is None:
                break
            parent_path.append(path_id)
            path_id = current.get("parentGroupID", None)
            if path_id is not None:
                current = sde_market_groups[path_id]
        parent_path.reverse()
        try:
            description = value["descriptionID"][lang]
        except KeyError:
            description = ""
        market_group = EAM.MarketGroup(
            group_id=key,
            name=value["nameID"][lang],
            description=description,
            has_types=value["hasTypes"],
            icon_id=value.get("iconID", -1),
            path=tuple(parent_path),
        )
        market_groups.data[market_group.group_id] = market_group
    return market_groups


def meta_groups(
    sde_meta_groups: dict[int, dict[str, Any]], lang: str = "en"
) -> EAM.MetaGroups:
    """Import meta groups from the SDE.

    Args:
        sde_meta_groups (dict[int, dict[str, Any]]): Dictionary of meta group data from SDE.
        lang (str, optional): Language code for names. Defaults to "en".

    Returns:
        EAM.MetaGroups: Collection of validated MetaGroup models.
    """
    argus_meta_groups = EAM.MetaGroups(data={})
    for key, value in sde_meta_groups.items():
        meta_group = EAM.MetaGroup(meta_id=key, name=value["nameID"][lang])
        argus_meta_groups.data[meta_group.meta_id] = meta_group
    return argus_meta_groups


def groups(sde_groups: dict[int, dict[str, Any]], lang: str = "en") -> EAM.Groups:
    """Import groups from the SDE.

    Args:
        sde_groups (dict[int, dict[str, Any]]): Dictionary of group data from SDE.
        lang (str, optional): Language code for names. Defaults to "en".

    Returns:
        EAM.Groups: Collection of validated Group models.
    """
    argus_groups = EAM.Groups(data={})
    for key, value in sde_groups.items():
        group = EAM.Group(
            group_id=key,
            anchorable=value["anchorable"],
            anchored=value["anchored"],
            category_id=value["categoryID"],
            fittable_non_singleton=value["fittableNonSingleton"],
            icon_id=value.get("iconID", -1),
            name=value["name"][lang],
            published=value["published"],
            use_base_price=value["useBasePrice"],
        )
        argus_groups.data[group.group_id] = group
    return argus_groups


def categories(
    sde_categories: dict[int, dict[str, Any]], lang: str = "en"
) -> EAM.Categories:
    """Import categories from the SDE.

    Args:
        sde_categories (dict[int, dict[str, Any]]): Dictionary of category data from SDE.
        lang (str, optional): Language code for names. Defaults to "en".

    Returns:
        EAM.Categories: Collection of validated Category models.
    """
    argus_categories = EAM.Categories(data={})
    for key, value in sde_categories.items():
        category = EAM.Category(
            category_id=key, name=value["name"][lang], published=value["published"]
        )
        argus_categories.data[category.category_id] = category
    return argus_categories
