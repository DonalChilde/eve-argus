"""Test for the industry calculation module."""

from pytest import raises

from eve_argus.data_transform import industry_base_calculations

ADJUSTED_PRICES = {
    34: 3.33,
    35: 16.47,
    36: 57.33,
    37: 286.12,
}

TRISTAN = {
    "base_materials": {
        34: 32000,
        35: 6000,
        36: 2500,
        37: 500,
    },
    "research_time": 2100,
    "manufacturing_time": 6000,
}

HOBGOBLIN = {
    "base_materials": {34: 509, 35: 7, 37: 4, 38: 2},
    "research_time": 105,
    "manufacturing_time": 300,
}


type_ids = {
    34: "Tritanium",
    35: "Pyrite",
    36: "Mexallon",
    37: "Isogen",
    38: "Nocxium",
    39: "Zydrine",
    40: "Megacyte",
}


def test_process_time_value() -> None:
    """Test the process_time_value function."""
    base_materials = TRISTAN["base_materials"].copy()
    adjusted_prices = ADJUSTED_PRICES.copy()
    research_time = TRISTAN["research_time"]
    beginning_runs = 0
    desired_runs = 10

    eiv = industry_base_calculations.eiv(
        base_materials=base_materials, adjusted_prices=adjusted_prices
    )
    time_req = industry_base_calculations.base_research_time(
        bp_time=research_time,
        beginning_runs=beginning_runs,
        desired_runs=desired_runs,
    )
    ptv = industry_base_calculations.process_time_value(
        time_required=time_req, eiv=eiv, base_time=research_time
    )
    expected = 23_979_399
    assert ptv == expected


def test_eiv() -> None:
    """Test the eiv function."""
    materials = TRISTAN["base_materials"].copy()
    adjusted_prices = ADJUSTED_PRICES.copy()

    # Test with base materials
    result = industry_base_calculations.eiv(materials, adjusted_prices)
    expected = 32000 * 3.33 + 6000 * 16.47 + 2500 * 57.33 + 500 * 286.12
    assert result == expected

    result = industry_base_calculations.eiv(materials, adjusted_prices, runs=2)
    expected = (32000 * 3.33 + 6000 * 16.47 + 2500 * 57.33 + 500 * 286.12) * 2
    assert result == expected

    # Test with empty materials
    result = industry_base_calculations.eiv({}, adjusted_prices)
    assert result == 0.0

    # Test with empty adjusted prices
    with raises(ValueError):
        result = industry_base_calculations.eiv(materials, {})
        assert result == 0.0

    # Test with no materials and no prices
    result = industry_base_calculations.eiv({}, {})
    assert result == 0.0


def test_base_research_time() -> None:
    """Test the process_time_value function."""
    bp_time = 105
    beginning_runs = 0
    desired_runs = 1
    expected = 105

    # Test with valid inputs
    result = industry_base_calculations.base_research_time(
        bp_time, beginning_runs, desired_runs
    )
    assert result == expected

    beginning_runs = 1
    desired_runs = 2
    expected = 145
    result = industry_base_calculations.base_research_time(
        bp_time, beginning_runs, desired_runs
    )
    assert result == expected

    beginning_runs = 0
    desired_runs = 10
    expected = 256000
    result = industry_base_calculations.base_research_time(
        bp_time, beginning_runs, desired_runs
    )
    assert result == expected


def test_manufacturing_time() -> None:
    """Test the manufacturing_time function."""
    base_time = TRISTAN["manufacturing_time"]
    runs = 1
    te = 0.0
    structure = 0.0
    skills = 0.32
    implants = 0.0
    rigs = 0.0

    result = industry_base_calculations.manufacturing_time(
        base_time=base_time,
        runs=runs,
        te=te,
        structure=structure,
        skills=skills,
        implants=implants,
        rigs=rigs,
    )
    expected = 60 * 68
    assert result == expected

    runs = 2
    result = industry_base_calculations.manufacturing_time(
        base_time=base_time,
        runs=runs,
        te=te,
        structure=structure,
        skills=skills,
        implants=implants,
        rigs=rigs,
    )
    expected = 60 * 68 * 2
    assert result == expected


def test_research_time() -> None:
    """Test the research_time function."""
    base_time = TRISTAN["research_time"]
    beginning_runs = 0
    desired_runs = 1
    structure = 0.0
    skills = 0.363
    implants = 0.0
    rigs = 0.0

    result = industry_base_calculations.research_time(
        base_time=base_time,
        beginning_runs=beginning_runs,
        desired_runs=desired_runs,
        structure=structure,
        skills=skills,
        implants=implants,
        rigs=rigs,
    )
    expected = 1338
    assert result == expected


def test_manufacturing_materials_required() -> None:
    """Test the manufacturing_materials_required function."""
    materials = TRISTAN["base_materials"].copy()
    runs = 1
    me = 0.0
    structure = 0.0
    rig = 0.0

    result = industry_base_calculations.manufacturing_materials_required(
        materials, runs, me, structure, rig
    )
    expected = TRISTAN["base_materials"]
    assert result == expected

    me = 0.1
    expected = {
        34: 28800,
        35: 5400,
        36: 2250,
        37: 450,
    }
    result = industry_base_calculations.manufacturing_materials_required(
        materials, runs, me, structure, rig
    )
    assert result == expected

    materials = HOBGOBLIN["base_materials"].copy()
    runs = 2
    me = 0.05
    expected = {
        34: 968,
        35: 14,
        37: 8,
        38: 4,
    }
    result = industry_base_calculations.manufacturing_materials_required(
        materials, runs, me, structure, rig
    )
    assert result == expected


def test_manufacturing_cost() -> None:
    """Test the manufacturing_cost function."""
    # 10NM Afterburner
    eiv = 60699
    system_cost_index = 0.02440
    structure_bonus = 0.0
    facility_tax = 0.0025
    scc = 0.04
    alpha_rate = 0.0025
    is_alpha = False

    result = industry_base_calculations.manufacturing_job_cost(
        eiv=eiv,
        system_cost_index=system_cost_index,
        structure_bonus=structure_bonus,
        facility_tax=facility_tax,
        scc=scc,
        alpha_rate=alpha_rate,
        is_alpha=is_alpha,
    )
    assert result["job_cost"] == 1481
    assert result["facility_tax"] == 152
    assert result["scc"] == 2428
    assert result["alpha"] == 0
    assert sum(result.values()) == 1481 + 152 + 2428 + 0  # type: ignore

    structure_bonus = 0.03

    result = industry_base_calculations.manufacturing_job_cost(
        eiv=eiv,
        system_cost_index=system_cost_index,
        structure_bonus=structure_bonus,
        facility_tax=facility_tax,
        scc=scc,
        alpha_rate=alpha_rate,
        is_alpha=is_alpha,
    )
    assert result["job_cost"] == 1437
    assert result["facility_tax"] == 152
    assert result["scc"] == 2428
    assert result["alpha"] == 0
    assert sum(result.values()) == 1437 + 152 + 2428 + 0  # type: ignore

    is_alpha = True

    result = industry_base_calculations.manufacturing_job_cost(
        eiv=eiv,
        system_cost_index=system_cost_index,
        structure_bonus=structure_bonus,
        facility_tax=facility_tax,
        scc=scc,
        alpha_rate=alpha_rate,
        is_alpha=is_alpha,
    )
    assert result["job_cost"] == 1437
    assert result["facility_tax"] == 152
    assert result["scc"] == 2428
    assert result["alpha"] == 152
    assert sum(result.values()) == 1437 + 152 + 2428 + 152  # type: ignore


def test_research_job_cost() -> None:
    """Test the research_job_cost function."""
    ptv = 24_413_974  # Example PTV for a research job
    system_cost_index = 0.0671
    structure_bonus = 0.0
    facility_tax = 0.0025
    scc = 0.02
    alpha_rate = 0.0025
    is_alpha = False

    result = industry_base_calculations.research_job_cost(
        ptv=ptv,
        system_cost_index=system_cost_index,
        structure_bonus=structure_bonus,
        facility_tax=facility_tax,
        scc=scc,
        alpha_rate=alpha_rate,
        is_alpha=is_alpha,
    )
    assert result["job_cost"] == 1638178
    assert result["facility_tax"] == 61035
    assert result["scc"] == 488279
    assert result["alpha"] == 0
    assert sum(result.values()) == 1638178 + 61035 + 488279 + 0  # type: ignore

    structure_bonus = 0.03

    result = industry_base_calculations.research_job_cost(
        ptv=ptv,
        system_cost_index=system_cost_index,
        structure_bonus=structure_bonus,
        facility_tax=facility_tax,
        scc=scc,
        alpha_rate=alpha_rate,
        is_alpha=is_alpha,
    )
    assert result["job_cost"] == 1589032
    assert result["facility_tax"] == 61035
    assert result["scc"] == 488279
    assert result["alpha"] == 0
    assert sum(result.values()) == 1589032 + 61035 + 488279 + 0  # type: ignore

    is_alpha = True

    result = industry_base_calculations.research_job_cost(
        ptv=ptv,
        system_cost_index=system_cost_index,
        structure_bonus=structure_bonus,
        facility_tax=facility_tax,
        scc=scc,
        alpha_rate=alpha_rate,
        is_alpha=is_alpha,
    )
    assert result["job_cost"] == 1589032
    assert result["facility_tax"] == 61035
    assert result["scc"] == 488279
    assert result["alpha"] == 61035
    assert sum(result.values()) == 1589032 + 61035 + 488279 + 61035  # type: ignore


def test_invention_job_cost() -> None:
    """Test the invention_job_cost function."""
    eiv = 877_250  # Example EIV for an invention job
    system_cost_index = 0.0507
    structure_bonus = 0.0
    facility_tax = 0.0025
    scc = 0.04
    alpha_rate = 0.0025
    is_alpha = False

    result = industry_base_calculations.invention_job_cost(
        eiv=eiv,
        system_cost_index=system_cost_index,
        structure_bonus=structure_bonus,
        facility_tax=facility_tax,
        scc=scc,
        alpha_rate=alpha_rate,
        is_alpha=is_alpha,
    )
    assert result["job_cost"] == 890
    assert result["facility_tax"] == 44
    assert result["scc"] == 702
    assert result["alpha"] == 0
    assert sum(result.values()) == 890 + 44 + 702 + 0  # type: ignore

    structure_bonus = 0.03

    result = industry_base_calculations.invention_job_cost(
        eiv=eiv,
        system_cost_index=system_cost_index,
        structure_bonus=structure_bonus,
        facility_tax=facility_tax,
        scc=scc,
        alpha_rate=alpha_rate,
        is_alpha=is_alpha,
    )
    assert result["job_cost"] == 863
    assert result["facility_tax"] == 44
    assert result["scc"] == 702
    assert result["alpha"] == 0
    assert sum(result.values()) == 863 + 44 + 702 + 0  # type: ignore

    is_alpha = True

    result = industry_base_calculations.invention_job_cost(
        eiv=eiv,
        system_cost_index=system_cost_index,
        structure_bonus=structure_bonus,
        facility_tax=facility_tax,
        scc=scc,
        alpha_rate=alpha_rate,
        is_alpha=is_alpha,
    )
    assert result["job_cost"] == 863
    assert result["facility_tax"] == 44
    assert result["scc"] == 702
    assert result["alpha"] == 44
    assert sum(result.values()) == 863 + 44 + 702 + 44  # type: ignore
