"""Functions get data from the EVE SDE."""

from eve_argus.models import static_data as SD


def types_in_market(eve_types: SD.EveTypes, only_published: bool) -> set[int]:
    """Get all type IDs that are in the market (i.e., have a market group).

    Args:
        eve_types: The EveTypes static data model.
        only_published: If True, only include published types.

    Returns:
        A set of type IDs that are in the market.
    """
    result = set()
    for type_id, type_obj in eve_types.data.items():
        if type_obj.marketGroupID is not None:
            if only_published and not type_obj.published:
                continue
            result.add(type_id)
    return result
