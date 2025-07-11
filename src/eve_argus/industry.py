from eve_argus.models import argus as EAM

from pydantic import BaseModel
from math import ceil


class ManufacturingMaterialsBonus(BaseModel):
    me: float = 1.0
    facility: float = 1.0


class ManufacturingTimeBonus(BaseModel):
    te: float = 1.0
    facility: float = 1.0
    skills: float = 1.0
    implants: float = 1.0


def manufacturing_time_required(
    blueprint: EAM.Blueprint, runs: int, bonus: ManufacturingTimeBonus
) -> int:
    """Calculate the time required for manufacturing a given blueprint.

    Args:
        blueprint (EAM.Blueprint): The blueprint for which time is required.
        runs (int): The number of runs to calculate time for.
        bonus (ManufacturingTimeBonus): The bonuses applied to manufacturing time.

    Returns:
        int: The total time required for manufacturing in seconds.

    Raises:
        ValueError: If the blueprint does not have manufacturing activities or time defined.
    """
    if (
        blueprint.activities.manufacturing is None
        or blueprint.activities.manufacturing.time is None
    ):
        raise ValueError(
            "Blueprint does not have manufacturing activities or time defined."
        )
    base_time = blueprint.activities.manufacturing.time
    adjusted_time = (
        base_time * bonus.te * bonus.facility * bonus.skills * bonus.implants
    )
    return ceil(adjusted_time * runs)


def manufacturing_materials_required(
    blueprint: EAM.Blueprint, runs: int, bonus: ManufacturingMaterialsBonus
) -> list[EAM.Material]:
    """Calculate the materials required for manufacturing a given blueprint.

    Args:
        blueprint (EAM.Blueprint): The blueprint for which materials are required.
        runs (int): The number of runs to calculate materials for.
        bonus (ManufacturingMaterialsBonus): The bonuses applied to material requirements.

    Returns:
        list[EAM.Material]: A list of materials required for manufacturing.

    Raises:
        ValueError: If the blueprint does not have manufacturing activities or materials defined.
    """
    materials_required: list[EAM.Material] = []
    if (
        blueprint.activities.manufacturing is None
        or blueprint.activities.manufacturing.materials is None
    ):
        raise ValueError(
            "Blueprint does not have manufacturing activities or materials defined."
        )
    for material in blueprint.activities.manufacturing.materials:
        qty = material.quantity * bonus.me * bonus.facility
        if qty < 1:
            qty = 1
        material_required = EAM.Material(
            typeID=material.typeID,
            quantity=ceil(qty * runs),
        )
        materials_required.append(material_required)
    return materials_required
