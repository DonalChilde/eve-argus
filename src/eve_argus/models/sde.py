"""Models for the Eve SDE."""

from typing import TypedDict


class Activities(TypedDict):
    pass


class Blueprint(TypedDict):
    blueprintTypeID: int
    maxProductionLimit: int
