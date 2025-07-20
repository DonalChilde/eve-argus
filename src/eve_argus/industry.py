from collections.abc import Sequence
from math import ceil
from uuid import UUID, uuid4

from pydantic import BaseModel

from eve_argus.models import argus as EAM

RESEARCH_TIME_MULTIPLIER = [
    1,
    29 / 21,
    23 / 7,
    39 / 5,
    278 / 15,
    928 / 21,
    2200 / 21,
    5251 / 21,
    4163 / 7,
    29660 / 21,
]


class JobMaterialsPrice(BaseModel):
    """Represents the material requirements and pricing for a job."""

    type_id: int
    quantity: int
    price: float


class JobMaterialsPriceProfile(BaseModel):
    """Collection of prices for materials.

    Can be used to calculate the ptv, eiv, and manufacturing materials costs for a job,
    depending on the profile used.

    """

    profile_id: UUID
    price_source: UUID
    description: str
    data: dict[int, JobMaterialsPrice]

    def total_price(self) -> float:
        """Calculate the total price of all materials in the profile."""
        return sum(
            job_materials.price * job_materials.quantity
            for job_materials in self.data.values()
        )


class ManufacturingMaterialsBonus(BaseModel):
    me: float = 1.0
    facility: float = 1.0


class ManufacturingTimeBonus(BaseModel):
    te: float = 1.0
    facility: float = 1.0
    skills: float = 1.0
    implants: float = 1.0


class ResearchTimeBonus(BaseModel):
    facility: float = 1.0
    skills: float = 1.0
    implants: float = 1.0


class ResearchCostFactors(BaseModel):
    system_cost_index: float = 0.0
    facility_tax: float = 0.0025
    scc_surcharge: float = 0.04
    alpha_tax: float = 0.0025
    structure_bonus: float = 1.0


class ManufacturingCostFactors(BaseModel):
    system_cost_index: float = 0.0
    facility_tax: float = 0.0025
    scc_surcharge: float = 0.04
    alpha_tax: float = 0.0025
    structure_bonus: float = 1.0


class ManufacturingCosts(BaseModel):
    # TODO can this be generalized for other jobs like invention and copying?

    job_cost: float
    facility: float
    scc: float
    alpha: float


class ResearchCosts(BaseModel):
    """Represents the cost breakdown of a research job."""

    job_cost: float
    facility: float
    scc: float
    alpha: float


# class MaterialsCost(BaseModel):
#     """Represents the cost of a material for a job."""

#     type_id: int
#     cost: float


# class JobCostProfile(BaseModel):
#     profile_id: UUID
#     description: str
#     data: dict[int, MaterialsCost]


# class JobCostProfiles(BaseModel):
#     """Collection of item cost profiles used by Jobs.

#     e.g. jits_buy_5, "job_unit_cost", etc.
#     """

#     data: dict[str, JobCostProfile]


# class JobMaterial(BaseModel):
#     type_id: int
#     quantity: int
#     price: float


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
            typeID=material.typeID,
            quantity=ceil(material.quantity),
        )
        materials_required.append(material_required)
    return materials_required


def calculate_eiv(
    materials: Sequence[EAM.Material], prices: EAM.UniverseMarketPrices
) -> int:
    """Calculate the estimated item value (EIV) based on materials."""
    # TODO test rounding behavior, is each calculation rounded or just the final result?
    eiv = 0.0
    for material in materials:
        eiv += material.quantity * prices.data[material.typeID].adjusted_price
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
        job_cost=round(
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
            typeID=material.typeID,
            quantity=ceil(qty * runs),
        )
        materials_required.append(material_required)
    return materials_required


def research_te_time(
    blueprint: EAM.Blueprint, runs: int, bonus: ResearchTimeBonus
) -> int:
    """Calculate the time required for researching a blueprint.

    Args:
        blueprint (EAM.Blueprint): The blueprint for which research time is required.
        runs (int): The number of runs to calculate time for.
        bonus (ResearchTimeBonus): The bonuses applied to research time.

    Returns:
        int: The total time required for research in seconds.

    Raises:
        ValueError: If the blueprint does not have research activities or time defined.
    """
    if (
        blueprint.activities.research_time is None
        or blueprint.activities.research_time.time is None
    ):
        raise ValueError("Blueprint does not have research activities or time defined.")
    base_time = blueprint.activities.research_time.time
    # FIXME this formula is incorrect. it probably needs starting run and ending run information.
    adjusted_time = base_time * bonus.facility * bonus.skills * bonus.implants
    return ceil(adjusted_time * runs)


def research_me_time(
    blueprint: EAM.Blueprint, runs: int, bonus: ResearchTimeBonus
) -> int:
    """Calculate the time required for researching a blueprint.

    Args:
        blueprint (EAM.Blueprint): The blueprint for which research time is required.
        runs (int): The number of runs to calculate time for.
        bonus (ResearchTimeBonus): The bonuses applied to research time.

    Returns:
        int: The total time required for research in seconds.

    Raises:
        ValueError: If the blueprint does not have research activities or time defined.
    """
    if (
        blueprint.activities.research_material is None
        or blueprint.activities.research_material.time is None
    ):
        raise ValueError("Blueprint does not have research activities or time defined.")
    base_time = blueprint.activities.research_material.time
    # FIXME this formula is incorrect. it probably needs starting run and ending run information.
    adjusted_time = base_time * bonus.facility * bonus.skills * bonus.implants
    return ceil(adjusted_time * runs)


def process_time_value(research_time: int, eiv: float) -> int:
    """Calculate the Process Time Value (PTV) based on bonuses and runs.

    https://wiki.eveuniversity.org/Research
    # TODO how is eiv calculated for this?

    Args:
        research_runs (int): The number of runs for the job.
        eiv (float): Estimated item value.

    Returns:
        int: The Process Time Value (PTV) for the job.
    """
    ptv = ceil(research_time * (0.02 / 105) * eiv)
    return ptv


def material_adjusted_price_profile(
    materials: Sequence[EAM.Material], universe_prices: EAM.UniverseMarketPrices
) -> JobMaterialsPriceProfile:
    """Combine the materials and their adjusted prices.

    Args:
        materials (Sequence[EAM.Material]): The materials to calculate the price for.
        universe_prices (EAM.UniverseMarketPrices): The universe prices for the materials.

    Returns:
        MaterialAdjustedPrices: A collection of adjusted prices for the materials.
    """
    adjusted_prices = JobMaterialsPriceProfile(
        profile_id=uuid4(),
        price_source=universe_prices.price_profile_id,
        description="Materials adjusted prices",
        data={},
    )

    for material in materials:
        adjusted_prices.data[material.typeID] = JobMaterialsPrice(
            type_id=material.typeID,
            quantity=material.quantity,
            price=material.quantity
            * universe_prices.data[material.typeID].adjusted_price,
        )
    return adjusted_prices


def copy_cost(
    cost_index: float,
    copies: int,
    runs_per_copy: int,
    eiv: float,
) -> float:
    """Calculate the cost of copying a blueprint based on cost index, number of copies, runs per copy, and eiv.

    https://wiki.eveuniversity.org/Research#Copying

    Args:
        cost_index (float): The cost index for the system.
        copies (int): The number of copies to be made.
        runs_per_copy (int): The number of runs per copy.
        eiv (float): Estimated item value.

    Returns:
        float: The total cost of the copying job.
    """
    total_cost = cost_index * copies * runs_per_copy * 0.02 * eiv
    return total_cost


def research_cost(
    ptv: float,
    system_cost_index: float,
    structure_bonus: float,
    facility_tax: float,
    scc_surcharge: float = 0.04,
    alpha_tax: float = 0.0025,
    isAlpha: bool = False,
) -> ResearchCosts:
    """Calculate the cost of researching a blueprint based on estimated item value and cost factors.

    https://wiki.eveuniversity.org/Research#The_cost_of_research

    #TODO is this round or ceil?

    Args:
        ptv (float): The Process Time Value for the job.
        system_cost_index (float): The cost index for the system.
        structure_bonus (float): The bonus applied by the structure.
        facility_tax (float): The tax applied by the facility.
        scc_surcharge (float): The surcharge applied by the SCC.
        alpha_tax (float): The tax applied for Alpha clones.
        isAlpha (bool): Whether the character is an Alpha clone.

    Returns:
        ResearchCosts: The total cost of the research job.
    """
    if isAlpha:
        alpha = round(ptv * alpha_tax)
    else:
        alpha = 0
    result = ResearchCosts(
        job_cost=round(ptv * (system_cost_index * structure_bonus)),
        facility=round(ptv * facility_tax),
        scc=round(ptv * scc_surcharge),
        alpha=alpha,
    )
    return result


def research_duration_base(base_time: int = 105, runs: int = 10) -> int:
    """Calculate the base duration for research based on the base time and number of runs.

    Args:
        base_time (int): The base time for the research job.
        runs (int): The number of runs for the research job.

    Returns:
        int: The total duration for the research job in seconds.
    """
    run_time = 105
    for i in range(1, 11):
        print(f"Run {i}: {run_time} seconds")
        run_time = ceil(run_time * (250 / 105))
    return ceil(run_time)


def research_time_diff(
    bp_time: int, initial_runs: int = 0, finished_runs: int = 10
) -> int:
    """Calculate the base time for research based on the blueprint time and runs.

    Args:
        bp_time (int): The base time for the blueprint.
        initial_runs (int): The number of initial runs.
        finished_runs (int): The number of finished runs.

    Returns:
        int: The total base time for the research job in seconds.
    """
    if initial_runs == 0:
        completed_time = 0
    else:
        completed_time = research_time(runs=initial_runs, base_time=bp_time)
    finished_time = research_time(runs=finished_runs, base_time=bp_time)
    diff_time = finished_time - completed_time
    return diff_time


def research_time(runs: int, base_time: int) -> int:
    """Calculate the total research time based on runs and base time.

    Argh damned eve math. Got research multipliers from fuzzworks blueprint calculator.
    Seems accurate.

    Args:
        runs (int): The number of runs for the research job.
        base_time (int): The base time for the research job.

    Returns:
        int: The total research time in seconds.
    """
    metime = 0
    for i in range(0, runs):
        metime = round(metime + (RESEARCH_TIME_MULTIPLIER[i] * base_time))
    return metime
