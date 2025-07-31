from uuid import uuid4

from eve_argus.models import argus as EAM


def type_id_subsets(
    type_infos: EAM.TypeInfos, groups: EAM.Groups, blueprints: EAM.Blueprints
) -> EAM.TypeIDSubsets:
    """Get type ID subsets from Argus data."""

    published = EAM.TypeIDSubset(
        description="published type_ids", type_ids=published_type_ids(type_infos)
    )
    published_blueprints = EAM.TypeIDSubset(
        description="published blueprints",
        type_ids=published_blueprints_type_ids(type_info=type_infos, groups=groups),
    )
    manufacturing_materials = EAM.TypeIDSubset(
        description="manufacturing materials",
        type_ids=manufacturing_materials_type_ids(blueprints=blueprints),
    )
    copy_materials = EAM.TypeIDSubset(
        description="copy materials",
        type_ids=copy_materials_type_ids(blueprints=blueprints),
    )
    reaction_materials = EAM.TypeIDSubset(
        description="reaction materials",
        type_ids=reaction_materials_type_ids(blueprints=blueprints),
    )
    research_materials = EAM.TypeIDSubset(
        description="research materials",
        type_ids=research_materials_type_ids(blueprints=blueprints),
    )
    invention_materials = EAM.TypeIDSubset(
        description="invention materials",
        type_ids=invention_materials_type_ids(blueprints=blueprints),
    )
    manufacturing_products = EAM.TypeIDSubset(
        description="manufacturing products",
        type_ids=manufacturing_products_type_ids(blueprints=blueprints),
    )
    reaction_products = EAM.TypeIDSubset(
        description="reaction products",
        type_ids=reaction_products_type_ids(blueprints=blueprints),
    )

    industry_related_type_ids: tuple[set[int], ...] = (
        published_blueprints.type_ids,
        manufacturing_materials.type_ids,
        copy_materials.type_ids,
        reaction_materials.type_ids,
        research_materials.type_ids,
        invention_materials.type_ids,
        manufacturing_products.type_ids,
        reaction_products.type_ids,
    )
    industry_related = EAM.TypeIDSubset(
        description="industry related type_ids",
        type_ids=set.union(*industry_related_type_ids),
    )
    types_in_market = EAM.TypeIDSubset(
        description="type_ids present in the market",
        type_ids=ids_in_market(
            type_info=type_infos, possible_type_ids=published.type_ids
        ),
    )
    argus_type_id_subsets = EAM.TypeIDSubsets(
        effective_date=type_infos.effective_date,
        data_set_id=uuid4(),
        data_type=EAM.DataTypes.TypeIDSubsets,
        data_source=type_infos.data_set_id,
        description="Argus type ID subsets",
        blueprints=published_blueprints,
        published=published,
        manufacturing_materials=manufacturing_materials,
        copy_materials=copy_materials,
        reaction_materials=reaction_materials,
        research_materials=research_materials,
        invention_materials=invention_materials,
        manufacturing_products=manufacturing_products,
        reaction_products=reaction_products,
        industry_related=industry_related,
        types_in_market=types_in_market,
    )
    return argus_type_id_subsets


def published_type_ids(type_info: EAM.TypeInfos) -> set[int]:
    """Get a set of published type IDs from TypeInfos."""
    return {
        type_id for type_id, type_data in type_info.data.items() if type_data.published
    }


def published_blueprints_type_ids(
    type_info: EAM.TypeInfos, groups: EAM.Groups
) -> set[int]:
    """Get a set of type IDs that are blueprints from TypeInfos."""
    result: set[int] = set()
    for type_id, type_data in type_info.data.items():
        if type_data.group_id is not None:
            group = groups.data.get(type_data.group_id)
            if (
                group is not None and group.category_id == 9
            ):  # Category ID for blueprints
                result.add(type_id)
    return result


def manufacturing_materials_type_ids(blueprints: EAM.Blueprints) -> set[int]:
    """Get a set of type IDs that are used in manufacturing materials."""
    result: set[int] = set()
    for blueprint in blueprints.data.values():
        activity = blueprint.activities.manufacturing
        if activity is not None and activity.materials is not None:
            # Add each material type ID to the result set
            for material in activity.materials:
                result.add(material.type_id)
    return result


def copy_materials_type_ids(blueprints: EAM.Blueprints) -> set[int]:
    """Get a set of type IDs that are used in copy materials."""
    result: set[int] = set()
    for blueprint in blueprints.data.values():
        activity = blueprint.activities.copying
        if activity is not None and activity.materials is not None:
            # Add each material type ID to the result set
            for material in activity.materials:
                result.add(material.type_id)
    return result


def invention_materials_type_ids(blueprints: EAM.Blueprints) -> set[int]:
    """Get a set of type IDs that are used in invention materials."""
    result: set[int] = set()
    for blueprint in blueprints.data.values():
        activity = blueprint.activities.invention
        if activity is not None and activity.materials is not None:
            # Add each material type ID to the result set
            for material in activity.materials:
                result.add(material.type_id)
    return result


def reaction_materials_type_ids(blueprints: EAM.Blueprints) -> set[int]:
    """Get a set of type IDs that are used in reaction materials."""
    result: set[int] = set()
    for blueprint in blueprints.data.values():
        activity = blueprint.activities.reaction
        if activity is not None and activity.materials is not None:
            # Add each material type ID to the result set
            for material in activity.materials:
                result.add(material.type_id)
    return result


def research_materials_type_ids(blueprints: EAM.Blueprints) -> set[int]:
    """Get a set of type IDs that are used in research materials."""
    result: set[int] = set()
    for blueprint in blueprints.data.values():
        activity = blueprint.activities.research_material
        if activity is not None and activity.materials is not None:
            # Add each material type ID to the result set
            for material in activity.materials:
                result.add(material.type_id)
        activity = blueprint.activities.research_time
        if activity is not None and activity.materials is not None:
            # Add each material type ID to the result set
            for material in activity.materials:
                result.add(material.type_id)
    return result


def manufacturing_products_type_ids(blueprints: EAM.Blueprints) -> set[int]:
    """Get a set of type IDs that are products of manufacturing."""
    result: set[int] = set()
    for blueprint in blueprints.data.values():
        activity = blueprint.activities.manufacturing
        if activity is not None and activity.products is not None:
            # Add each product type ID to the result set
            for product in activity.products:
                result.add(product.type_id)
    return result


def reaction_products_type_ids(blueprints: EAM.Blueprints) -> set[int]:
    """Get a set of type IDs that are products of reactions."""
    result: set[int] = set()
    for blueprint in blueprints.data.values():
        activity = blueprint.activities.reaction
        if activity is not None and activity.products is not None:
            # Add each product type ID to the result set
            for product in activity.products:
                result.add(product.type_id)
    return result


def ids_in_market(type_info: EAM.TypeInfos, possible_type_ids: set[int]) -> set[int]:
    """Subset of type IDs that are in the market."""
    result: set[int] = set()
    for type_id in possible_type_ids:
        if (
            type_info.data.get(type_id) is not None
            and type_info.data[type_id].market_group_id is not None
        ):
            result.add(type_id)
    return result
