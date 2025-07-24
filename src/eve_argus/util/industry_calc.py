"""Industry calculations using the most basic inputs."""

from math import ceil, floor
from typing import TypedDict

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


# TODO at this level, can one cost dict cover all the actions?
class ManufacturingCosts(TypedDict):
    """TypedDict for manufacturing costs."""

    job_cost: float
    facility_tax: float
    scc: float
    alpha: float


class ResearchCosts(TypedDict):
    """TypedDict for research costs."""

    job_cost: float
    facility_tax: float
    scc: float
    alpha: float


class CopyCosts(TypedDict):
    """TypedDict for copy costs."""

    job_cost: float
    facility_tax: float
    scc: float
    alpha: float


class InventionCosts(TypedDict):
    """TypedDict for invention costs."""

    job_cost: float
    facility_tax: float
    scc: float
    alpha: float


class ReactionCosts(TypedDict):
    """TypedDict for reaction costs."""

    job_cost: float
    facility_tax: float
    scc: float
    alpha: float


def copy_cost() -> float:
    """Returns the cost of copying a blueprint."""
    # TODO stub
    return 0.0


def invention_cost() -> float:
    """Returns the cost of inventing a blueprint."""
    # TODO stub
    return 0.0


def reaction_cost() -> float:
    """Returns the cost of reacting a blueprint."""
    # TODO stub
    return 0.0


def research_cost() -> float:
    """Returns the cost of researching a blueprint."""
    # TODO stub
    return 0.0


def eiv(materials: dict[int, int], adjusted_prices: dict[int, float]) -> float:
    """Calculates the estimated industry value (EIV) of a set of materials."""
    total_value = 0.0
    for material_id, quantity in materials.items():
        if material_id in adjusted_prices:
            total_value += adjusted_prices[material_id] * quantity
        else:
            raise ValueError(
                f"Material ID {material_id} not found in adjusted_prices dictionary."
            )
    return total_value


def process_time_value(time_required: int, eiv: float) -> int:
    """Calculates the process time value (PTV) based on the time required and EIV."""
    ptv = ceil(time_required * (0.02 / 105) * eiv)
    return ptv


def manufacturing_materials_required(
    materials: dict[int, int], runs: int, me: float, facility: float, rig: float
) -> dict[int, int]:
    """Calculates the materials required for a manufacturing job."""
    # TODO validate math
    if runs < 1:
        raise ValueError("Runs must be one or greater.")

    required_materials = {}
    for material_id, quantity in materials.items():
        req_mats = quantity * (1 - me) * (1 - facility) * (1 - rig)
        if req_mats < 0:
            req_mats = 1
        required_materials[material_id] = ceil(req_mats * runs)
    return required_materials


def manufacturing_job_cost(
    eiv: float,
    system_cost_index: float,
    structure_bonus: float = 0.0,
    facility_tax: float = 0.0,
    scc: float = 0.04,
    alpha_rate: float = 0.0025,
    is_alpha: bool = False,
) -> ManufacturingCosts:
    """Calculates the cost of a manufacturing job."""
    if eiv < 0:
        raise ValueError("Estimated Industry Value (EIV) must be non-negative.")

    job_cost = round(eiv * (system_cost_index * structure_bonus))
    if is_alpha:
        alpha = round(eiv * alpha_rate)
    else:
        alpha = 0
    facility = round(eiv * facility_tax)
    scc = round(eiv * scc)

    result = ManufacturingCosts(
        job_cost=job_cost, facility_tax=facility, scc=scc, alpha=alpha
    )

    return result


def manufacturing_time(
    base_time: int,
    te: float,
    facility: float,
    skills: float,
    implants: float,
    runs: int,
) -> int:
    """Calculates the manufacturing time for a job."""
    if runs < 1:
        raise ValueError("Runs must be one or greater.")
    # TODO see if math checks out, add note that zero tax rate can be used if missing value.
    elapsed = base_time / (1 + te) / (1 + facility) / (1 + skills) / (1 + implants)
    elapsed = ceil(elapsed * runs)

    return elapsed


def research_te_time(
    base_time: int,
    runs_completed: int,
    runs: int,
    skills: float,
    implants: float,
    facility: float,
    rigs: float,
) -> int:
    """Calculates the time required for a research job."""
    # TODO validate math and inputs
    base_required = base_research_time(
        bp_time=base_time, beginning_runs=runs_completed, desired_runs=runs
    )

    time_required = (
        base_required / (1 + skills) / (1 + implants) / (1 + facility) / (1 + rigs)
    )
    time_required = ceil(time_required * runs)

    return time_required


def research_me_time() -> int:
    """Returns the time required for a material efficiency research job."""
    # TODO stub
    return 0


def base_research_time(
    bp_time: int, beginning_runs: int = 0, desired_runs: int = 10
) -> int:
    """Calculate the base time for research based on the blueprint time and runs.

    Args:
        bp_time (int): The base time for the blueprint.
        beginning_runs (int): The number of beginning runs, runs already done.
        desired_runs (int): The desired number of runs for the research job.

    Returns:
        int: The total base time for the research job in seconds.
    """
    if beginning_runs == 0:
        already_completed_time = 0
    else:
        already_completed_time = _research_time(runs=beginning_runs, base_time=bp_time)
    desired_time = _research_time(runs=desired_runs, base_time=bp_time)

    return desired_time - already_completed_time


def _research_time(runs: int, base_time: int) -> int:
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
