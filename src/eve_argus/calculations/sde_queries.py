"""Functions get data from the EVE SDE."""

from eve_argus.models import static_data as SD


def get_market_path_int(
    market_group_id: int, market_groups: SD.MarketGroups
) -> list[int]:
    """Get the market path as a list of integers for a given market group ID.

    Starting from the given market group ID, traverse up the parentGroupIDs
    to build the full path to the root market group. Path is returned as a list
    of integers representing market group IDs from root to the specified market group.
    """
    if market_group_id not in market_groups.data:
        raise ValueError(
            f"Market group ID {market_group_id} not found in market groups."
        )

    def get_path(market_group_id: int) -> list[int]:
        path = []
        current = market_groups.data.get(market_group_id)
        while current:
            path.append(current._key)
            if current.parentGroupID is None:
                break
            current = market_groups.data.get(current.parentGroupID)
        return path

    path = get_path(market_group_id)
    if not path:
        raise ValueError(
            f"Market group ID {market_group_id} not found in market groups."
        )
    return list(reversed(path))


def get_market_path_string(
    market_path: list[int], market_groups: SD.MarketGroups, separator: str = "/"
) -> str:
    """Get the market path as a string for a given market path list of integers."""
    names = []
    for mg_id in market_path:
        market_group = market_groups.data.get(mg_id)
        if market_group is None:
            raise ValueError(f"Market group ID {mg_id} not found in market groups.")
        names.append(market_group.name)
    return separator.join(names)
