"""The models to represent an industry job in EVE Argus."""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from eve_argus.models import argus as EAM


class MaterialsPrice(BaseModel):
    """Represents the material pricing for a job."""

    type_id: int
    price: float


class MaterialsPriceProfile(BaseModel):
    """Collection of prices for materials.

    Can be used to calculate the ptv, eiv, and manufacturing materials costs for a job,
    depending on the profile used.

    """

    profile_id: UUID
    price_source: UUID
    source_type: Literal["adjusted", "market", "sub_assembly"]
    description: str
    data: dict[int, MaterialsPrice]

    def price(self, type_id: int) -> float:
        """Get the price for a specific type_id.

        Currently returns -1.0 if type_id is not found
        """
        return self.data[type_id].price if type_id in self.data else -1.0


class JobBlueprint(BaseModel):
    """Represents a blueprint used in a job."""

    blueprint_type_id: int
    product_type_id: int
    """The type_id of the product produced by the blueprint."""
    material_efficiency: int
    time_efficiency: int
    runs: int
    base_build_time: int
    """The build time in seconds."""
    portion_size: int
    """The amount of the product produced per run."""


class StructureConfig(BaseModel):
    """Represents the configuration of a structure used in a job."""

    config_id: UUID
    structure_id: int | None = None
    """The ID of the structure, if applicable. None if no structure is used."""
    structure_type: Literal["NPC", "STRUCTURE"] = "NPC"
    me_bonus: float = 0.0
    """Material efficiency bonus provided by the structure."""
    te_bonus: float = 0.0
    """Time efficiency bonus provided by the structure."""
    research_bonus: float = 0.0
    """Research bonus provided by the structure."""
    cost_bonus: float = 0.0
    """Cost bonus provided by the structure."""
    tax_rate: float = 0.0
    """Tax rate applied by the structure."""
    rig_me_bonus: float = 0.0
    """Material efficiency bonus from structure rigs."""
    rig_te_bonus: float = 0.0
    """Time efficiency bonus from structure rigs."""
    rig_effective: list[str] = []
    """categories of products that are affected by the structure's rigs."""


class JobLocation(BaseModel):
    """Represents the location where a job is executed."""

    location_profile_id: UUID
    """The ID of the location profile used for the job."""
    system_id: int
    structure: StructureConfig
    """The structure configuration used for the job."""


class JobCharacter(BaseModel):
    """Represents the character related information for a job, e.g. skills and implants."""

    character_profile_id: UUID
    """The ID of the character profile used for the job."""
    character_id: int | None = None
    corporation_id: int | None = None
    skills: dict[str, int] = {}  # skill_name: skill_level
    implants: list[str] = []  # implants
    manufacturing_te_bonus_skills: float = 0.0  # time efficiency bonus
    manufacturing_te_bonus_implants: float = 0.0  # time efficiency bonus from implants
    research_te_bonus_skills: float = 0.0  # time efficiency bonus
    research_te_bonus_implants: float = 0.0  # time efficiency bonus from


class ManufacturingJobCosts(BaseModel):
    """Represents the costs associated with a manufacturing job."""

    eiv: float = 0.0
    """Effective Item Value, the value of the items produced by the job."""
    facility_tax: float = 0.0
    alpha_tax: float = 0.0
    scc_tax: float = 0.0


class InventionJobCosts(BaseModel):
    """Represents the costs associated with an invention job."""

    eiv: float = 0.0
    """Effective Item Value, the value of the items produced by the job."""
    job_base_cost: float = 0.0
    """Base cost of the invention job."""
    facility_tax: float = 0.0
    alpha_tax: float = 0.0
    scc_tax: float = 0.0


class ResearchJobCosts(BaseModel):
    """Represents the costs associated with a research job."""

    eiv: float = 0.0
    """Effective Item Value, the value of the items produced by the job."""
    ptv: float = 0.0
    """Processing Time Value, the value of the time spent on the job."""
    facility_tax: float = 0.0
    alpha_tax: float = 0.0
    scc_tax: float = 0.0


class CopyJobCosts(BaseModel):
    """Represents the costs associated with a copy job."""

    eiv: float = 0.0
    """Effective Item Value, the value of the items produced by the job."""

    facility_tax: float = 0.0
    alpha_tax: float = 0.0
    scc_tax: float = 0.0


class JobMaterial(BaseModel):
    """Represents a material used in a job."""

    type_id: int
    quantity: int


class JobMaterials(BaseModel):
    """Represents the materials used in a job."""

    materials: dict[int, JobMaterial] = {}
    """The materials used in the job, keyed by type_id."""


class ManufacturingJob(BaseModel):
    """Represents a manufacturing job."""

    job_id: UUID
    notes: str = ""
    blueprint: JobBlueprint
    location: JobLocation
    """Location profile where the job is executed."""
    character: JobCharacter
    """Character profile used for the job, e.g. skills and implants."""
    sub_assemblies: list[UUID] = []
    """List of sub-assembly job IDs, if any."""

    # These fields  will change based on the current conditions.
    system_cost_index: EAM.SystemCostIndex
    materials_adjusted_prices: MaterialsPriceProfile
    materials_market_prices: MaterialsPriceProfile

    # This field depends on the blueprint, and location.
    materials_required: JobMaterials
    """The materials required for the job, keyed by type_id. Does not include sub-assemblies."""

    # This field depends on blueprint, location, system_cost_index, and materials_adjusted_prices fields.
    costs: ManufacturingJobCosts
    """The costs associated with the job, including EIV, facility tax, alpha tax, and SCC tax."""

    # This field depends on the blueprint, location, and character fields.
    build_time: int = -1
    """The build time in seconds, -1 if not calculated yet."""


class ResearchJob(BaseModel):
    """Represents a research job."""

    job_id: UUID
    notes: str = ""
    blueprint: JobBlueprint
    location: JobLocation
    """Location profile where the job is executed."""
    character: JobCharacter
    """Character profile used for the job, e.g. skills and implants."""

    # These fields will change based on the current conditions.
    system_cost_index: EAM.SystemCostIndex
    materials_adjusted_prices: MaterialsPriceProfile
    materials_market_prices: MaterialsPriceProfile

    # This field depends on the blueprint.
    materials_required: JobMaterials
    """The materials required for the job, keyed by type_id. Does not include sub-assemblies."""

    # This field depends on blueprint, location, system_cost_index, and materials_adjusted_prices fields.
    costs: ResearchJobCosts
    """The costs associated with the job, including EIV, facility tax, alpha tax, and SCC tax."""

    # This field depends on the blueprint, location, and character fields.
    build_time: int = -1
    """The build time in seconds, -1 if not calculated yet."""


class InventionJob(BaseModel):
    """Represents an invention job."""

    job_id: UUID
    notes: str = ""
    blueprint: JobBlueprint
    location: JobLocation
    """Location profile where the job is executed."""
    character: JobCharacter
    """Character profile used for the job, e.g. skills and implants."""

    # These fields will change based on the current conditions.
    system_cost_index: EAM.SystemCostIndex
    materials_adjusted_prices: MaterialsPriceProfile
    materials_market_prices: MaterialsPriceProfile

    # This field depends on the blueprint.
    materials_required: JobMaterials
    """The materials required for the job, keyed by type_id. Does not include sub-assemblies."""

    # This field depends on blueprint, location, system_cost_index, and materials_adjusted_prices fields.
    costs: InventionJobCosts
    """The costs associated with the job, including EIV, facility tax, alpha tax, and SCC tax."""

    # This field depends on the blueprint, location, and character fields.
    build_time: int = -1
    """The build time in seconds, -1 if not calculated yet."""


class CopyJob(BaseModel):
    """Represents a copy job."""

    job_id: UUID
    notes: str = ""
    blueprint: JobBlueprint
    location: JobLocation
    """Location profile where the job is executed."""
    character: JobCharacter
    """Character profile used for the job, e.g. skills and implants."""

    # These fields will change based on the current conditions.
    system_cost_index: EAM.SystemCostIndex
    materials_adjusted_prices: MaterialsPriceProfile
    materials_market_prices: MaterialsPriceProfile

    # This field depends on the blueprint.
    materials_required: JobMaterials
    """The materials required for the job, keyed by type_id. Does not include sub-assemblies."""

    # This field depends on blueprint, location, system_cost_index, and materials_adjusted_prices fields.
    costs: CopyJobCosts
    """The costs associated with the job, including EIV, facility tax, alpha tax, and SCC tax."""

    # This field depends on the blueprint, location, and character fields.
    build_time: int = -1
    """The build time in seconds, -1 if not calculated yet."""


def materials_required(blueprint: JobBlueprint, location: JobLocation) -> JobMaterials:
    """Calculate the materials required for a job based on the blueprint and location."""
    # This function would typically calculate the materials required based on the blueprint,
    # location, and any other relevant factors such as skills, implants, etc.
    # For now, it returns an empty JobMaterials instance.
    return JobMaterials(materials={})


def manufacturing_job_costs(
    blueprint: JobBlueprint,
    location: JobLocation,
    materials: JobMaterials,
    materials_adjusted_prices: MaterialsPriceProfile,
) -> ManufacturingJobCosts:
    """Calculate the costs for a manufacturing job based on the blueprint, location, and material prices."""
    # This function would typically calculate the costs based on the blueprint, location,
    # and materials prices. For now, it returns an empty ManufacturingJobCosts instance.
    pass


def manufacturing_build_time(
    blueprint: JobBlueprint,
    location: JobLocation,
    character: JobCharacter,
) -> int:
    """Calculate the build time for a job based on the blueprint, location, and character."""
    # This function would typically calculate the build time based on the blueprint,
    # location, and any other relevant factors such as skills, implants, etc.
    # For now, it returns -1 to indicate that the build time is not calculated yet.
    return -1


# TODO function to find type_ids blueprints with no sub-assemblies
# TODO algorithm to calculate sub-assemblies with sub-assemblies - what needs to be done first?
# TODO function to determine if a blueprint has sub-assemblies
# TODO function to determine if a type_id is the product of a blueprint.
# TODO function to compile all type_ids that are the product of a blueprint.
# TODO function to compile products of a blueprint that are used in other blueprints - is a sub-assembly.

# 1. get character profile.
# 2. get location profile.
# 3. get blueprint profile.
# 4. get job materials.
# 5. get sub-assembly jobs - see if sub-assembly has already been calculated.
# 6. get prices
# 7. calculate jobs costs.
# 8. calculate build time.
