"""Utility functions for working with argus models."""

from collections.abc import Iterable
from eve_argus.models import argus as EAM


def published_typeIDs(type_dict: EAM.TypeInfoDict) -> Iterable[int]:
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
    for item in type_dict.data.values():
        if item.published:
            yield item.typeID
