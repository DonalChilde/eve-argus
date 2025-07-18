"""Utility functions for working with argus models."""

from collections.abc import Iterable, Sequence
from eve_argus.models import argus as EAM


def published_type_ids(type_dict: EAM.TypeInfoDict) -> Sequence[int]:
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
    published: list[int] = []
    for item in type_dict.data.values():
        if item.published:
            published.append(item.type_id)
    return published


def get_type_ids_used_in_blueprints(blueprints: EAM.BlueprintsDict) -> Sequence[int]:
    type_ids: set[int] = set()
    for blueprint in blueprints.data.values():
        if blueprint.activities.copying:
            for material in blueprint.activities.copying.materials:
                type_ids.add(material.typeID)
        if blueprint.activities.invention:
            for material in blueprint.activities.invention.materials:
                type_ids.add(material.typeID)
            for material in blueprint.activities.invention.products:
                type_ids.add(material.typeID)
        if blueprint.activities.manufacturing:
            for material in blueprint.activities.manufacturing.materials:
                type_ids.add(material.typeID)
            for material in blueprint.activities.manufacturing.products:
                type_ids.add(material.typeID)
        if blueprint.activities.research_material:
            for material in blueprint.activities.research_material.materials:
                type_ids.add(material.typeID)
        if blueprint.activities.research_time:
            for material in blueprint.activities.research_time.materials:
                type_ids.add(material.typeID)

    return list(type_ids)
