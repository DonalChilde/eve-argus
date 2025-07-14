from collections.abc import Sequence
from uuid import UUID
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


class ManufacturingCostFactors(BaseModel):
    system_cost_index: float = 0.0
    facility_tax: float = 0.0025
    scc_surcharge: float = 0.04
    alpha_tax: float = 0.0025
    structure_bonus: float = 1.0


class ManufacturingCosts(BaseModel):
    # TODO can this be generalized for other jobs like invention and copying?

    base_cost: int
    facility: int
    scc: int
    alpha: int


class MaterialsCost(BaseModel):
    """Represents the cost of a material for a job."""

    type_id: int
    cost: float


class JobCostProfile(BaseModel):
    profile_id: UUID
    description: str
    data: dict[int, MaterialsCost]


class JobCostProfiles(BaseModel):
    """Collection of item cost profiles used by Jobs.

    e.g. jits_buy_5, "job_unit_cost", etc.
    """

    data: dict[str, JobCostProfile]


class JobMaterial(BaseModel):
    type_id: int
    quantity: int
    price: float


# TODO decide wether to use UUID or str for ids. UUIDs seem fine for dict keys and pydantic. And should be smaller in memory than strings.
class LocationProfile(BaseModel):
    """Location information for industry jobs.

    eg, region, station, system cost indexes, rigs, security, etc.
    """

    profile_id: UUID


class CharacterProfile(BaseModel):
    """Character based information for industry jobs.

    eg, skills, implants
    """

    profile_id: UUID


class IndustryJob(BaseModel):
    """The minimum information required to describe the result of an industry job.

    job costs, materials required, and time required will vary based on system, skills,
    implants, and station.
    """

    job_uuid: UUID
    blueprint_type_id: int
    runs: int
    me: int
    te: int
    result_type_id: int
    result_qty: int
    activity_type: str
    unit_cost: float
    job_costs: ManufacturingCosts
    materials_cost: float
    eiv: float
    location_profile: UUID
    character_profile: UUID
    cost_profile: UUID
    materials_required: list[JobMaterial] = []
    time_required: int


# TODO use CharacterProfile and LocationProfile to pass infomation to functions.


def calculate_copy_cost(blueprint: EAM.Blueprint, runs: int) -> float:
    """Calculate the cost of copying a blueprint based on runs and cost factors."""
    # WARNING: This is a generated stub, and the formula is not accurate.
    # Need to check for modifiers, like skills and implants.
    if (
        blueprint.activities.copying is None
        or blueprint.activities.copying.cost is None
    ):
        raise ValueError("Blueprint does not have copying activities or cost defined.")
    base_cost = blueprint.activities.copying.cost
    return base_cost * runs


def calculate_invention_materials(blueprint: EAM.Blueprint) -> list[EAM.Material]:
    """Calculate the materials required for invention based on the blueprint."""
    # WARNING: This is a generated stub, and the formula is not accurate.
    # Need to check for modifiers, like skills and implants.
    materials_required: list[EAM.Material] = []
    if (
        blueprint.activities.invention is None
        or blueprint.activities.invention.materials is None
    ):
        raise ValueError(
            "Blueprint does not have invention activities or materials defined."
        )
    for material in blueprint.activities.invention.materials:
        material_required = EAM.Material(
            type_id=material.type_id,
            quantity=ceil(material.quantity),
        )
        materials_required.append(material_required)
    return materials_required


def calculate_eiv(
    materials: Sequence[EAM.Material], prices: EAM.MarketPricesUniverseDict
) -> int:
    """Calculate the estimated item value (EIV) based on materials."""
    # TODO test rounding behavior, is each calculation rounded or just the final result?
    eiv = 0.0
    for material in materials:
        eiv += material.quantity * prices.data[material.type_id].adjusted_price
    return round(eiv)


def manufacturing_job_cost(
    eiv: float, cost_factors: ManufacturingCostFactors, isAlpha: bool = False
) -> ManufacturingCosts:
    """Calculate the cost of a manufacturing job based on runs, estimated item value, and cost factors.

    https://wiki.eveuniversity.org/Manufacturing
    Args:
        eiv (float): Estimated item value.
        cost_factors (ManufacturingCostFactors): The cost factors affecting the job cost.

    Returns:
        ManufacturingCostBreakdown: The total cost of the manufacturing job.
    """
    if isAlpha:
        alpha = round(eiv * cost_factors.alpha_tax)
    else:
        alpha = 0
    result = ManufacturingCosts(
        base_cost=round(
            eiv * (cost_factors.system_cost_index * cost_factors.structure_bonus)
        ),
        facility=round(eiv * cost_factors.facility_tax),
        scc=round(eiv * cost_factors.scc_surcharge),
        alpha=alpha,
    )
    return result


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
            type_id=material.type_id,
            quantity=ceil(qty * runs),
        )
        materials_required.append(material_required)
    return materials_required
