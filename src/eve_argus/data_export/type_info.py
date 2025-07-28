"""This module provides functionality to create a table of type information."""

from collections.abc import Iterable, Sequence
from typing import Any

from eve_argus.models import argus as EAM


def type_info_table(
    type_info: EAM.TypeInfos,
    meta_levels: EAM.MetaGroups,
    groups: EAM.Groups,
    categories: EAM.Categories,
    market_groups: EAM.MarketGroups,
    type_ids: Iterable[int] | None = None,
) -> Sequence[dict[str, Any]]:
    """Create a table of type information."""
    table = []
    if type_ids is None:
        type_ids = type_info.data.keys()
    for type_id in type_ids:
        info = type_info.data[type_id]
        meta = meta_levels.data.get(info.meta_group_id) if info.meta_group_id else None
        group = groups.data.get(info.group_id) if info.group_id else None
        category = categories.data.get(group.category_id) if group else None
        market_group = (
            market_groups.data.get(info.market_group_id)
            if info.market_group_id
            else None
        )

        table.append(
            {
                "Type ID": type_id,
                "Name": info.name,
                "Meta Level": meta.name if meta else "N/A",
                "Category": category.name if category else "N/A",
                "Group": group.name if group else "N/A",
                "Market Group": market_group.name if market_group else "N/A",
                "Portion Size": info.portion_size,
                "Capacity": info.capacity if info.capacity is not None else "N/A",
                "Market Path": market_groups.path_string(
                    market_group.path if market_group else [],
                    separator="\\",
                ),
            }
        )
    return table
