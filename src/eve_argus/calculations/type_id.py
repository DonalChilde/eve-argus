"""Utility functions for working with argus models."""

from eve_argus.models import argus as EAM


def published_type_ids(type_dict: EAM.TypeInfos) -> EAM.TypeIDSubset:
    """published_typeIDs .

    Args:
        type_dict (EAM.TypeInfoDict): _description_

    Returns:
        Iterable[int]: _description_

    Yields:
        Iterator[Iterable[int]]: _description_
    """
    # A bit of unnecessary right now, as unpublished types are filtered by default.
    # Keep this until I figure out if any of the unpublished types are needed...
    published: set[int] = set()
    for item in type_dict.data.values():
        if item.published:
            published.add(item.type_id)
    result = EAM.TypeIDSubset(description="Published type IDs", type_ids=published)
    return result


def type_ids_used_in_blueprints(
    blueprints: EAM.Blueprints, published_type_ids: EAM.TypeIDSubset | None = None
) -> EAM.TypeIDSubset:
    type_ids: set[int] = set()
    for blueprint in blueprints.data.values():
        type_ids.add(blueprint.blueprintTypeID)
        if blueprint.activities.copying:
            for material in blueprint.activities.copying.materials:
                type_ids.add(material.type_id)
        if blueprint.activities.invention:
            for material in blueprint.activities.invention.materials:
                type_ids.add(material.type_id)
            for material in blueprint.activities.invention.products:
                type_ids.add(material.type_id)
        if blueprint.activities.manufacturing:
            for material in blueprint.activities.manufacturing.materials:
                type_ids.add(material.type_id)
            for material in blueprint.activities.manufacturing.products:
                type_ids.add(material.type_id)
        if blueprint.activities.research_material:
            for material in blueprint.activities.research_material.materials:
                type_ids.add(material.type_id)
        if blueprint.activities.research_time:
            for material in blueprint.activities.research_time.materials:
                type_ids.add(material.type_id)
    if published_type_ids is not None:
        type_ids = type_ids.intersection(published_type_ids.type_ids)
        descriptor = "Type IDs used in blueprints, filtered by published types."
    else:
        descriptor = "Type IDs used in blueprints, published and unpublished."
    result = EAM.TypeIDSubset(
        description=descriptor,
        type_ids=type_ids,
    )
    return result


def type_ids_possible_in_market(
    eve_types: EAM.TypeInfos, filter_published: bool | None = True
) -> EAM.TypeIDSubset:
    """Get type IDs possible in the market from the SDE data."""
    if filter_published is not None:
        type_ids = [
            x.type_id
            for x in eve_types.data.values()
            if (x.market_group_id is not None and x.published == filter_published)
        ]
    else:
        type_ids = [
            x.type_id for x in eve_types.data.values() if x.market_group_id is not None
        ]
    return EAM.TypeIDSubset(
        description=f"Type IDs that are possible in the market, published filter = {filter_published}",
        type_ids=set(type_ids),
    )


def type_ids_needed_for_industry_pricing(
    market_type_ids: EAM.TypeIDSubset,
    blueprint_type_ids: EAM.TypeIDSubset,
) -> EAM.TypeIDSubset:
    """Get type IDs needed for industry pricing."""
    type_ids = market_type_ids.type_ids.intersection(blueprint_type_ids.type_ids)

    return EAM.TypeIDSubset(
        description="Type IDs needed for industry pricing.",
        type_ids=type_ids,
    )


def type_ids_of_blueprints(
    type_info: EAM.TypeInfos, groups: EAM.Groups
) -> EAM.TypeIDSubset:
    """Get type IDs of blueprints."""
    type_ids = set()
    for info in type_info.data.values():
        if info.group_id is not None:
            group = groups.data.get(info.group_id)
            if group is not None and group.category_id == 9:
                type_ids.add(info.type_id)

    return EAM.TypeIDSubset(
        description="Type IDs of blueprints.",
        type_ids=type_ids,
    )
