"""Industry jobs model."""

# This is another version of the industry jobs model.
# This model focuses on deduplication of the data, and separating the different
# structures enough that different scenarios can be run with minimal changes.

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
    product_type_id: int  # TODO handle one blueprint makes multiple things. is this only an invention thing?
    """The type_id of the product produced by the blueprint."""
    material_efficiency: int
    time_efficiency: int
    runs: int
    base_build_time: int
    """The build time in seconds."""
    portion_size: int
    """The amount of the product produced per run."""
    max_runs: int
    """The maximum number of runs that can be performed with this blueprint."""


class CharacterProfile(BaseModel):
    """The character related info needed for an industry job."""

    profile_id: UUID
    character_id: int | None = None
    corporation_id: int | None = None
    skills: dict[str, int] = {}  # skill_name: skill_level
    implants: list[str] = []  # implants
    manufacturing_te_bonus_skills: float = 0.0  # time efficiency bonus
    manufacturing_te_bonus_implants: float = 0.0  # time efficiency bonus from implants
    research_te_bonus_skills: float = 0.0  # time efficiency bonus
    research_te_bonus_implants: float = 0.0  # time efficiency bonus from implants


class StructureProfile(BaseModel):
    """The structure related info needed for an industry job."""

    profile_id: UUID
    structure_id: int | None = None
    """The ID of the structure, if applicable. None if no specific structure is used."""
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


class LocationProfile(BaseModel):
    """The location related info needed for an industry job."""

    location_id: UUID
    solar_system_id: int
    region_id: int
    system_cost_index: dict[str, float] = {}
    """Cost index for the system, keyed by activity type (e.g., 'manufacturing', 'research')."""


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
    """A Manufacturing job."""

    job_id: UUID
    notes: str = ""
    blueprint: JobBlueprint
    location: UUID
    """Location profile where the job is executed."""
    structure: UUID
    """Structure profile used for the job, e.g. a citadel or NPC station."""
    character: UUID
    """Character profile used for the job, e.g. skills and implants."""
    sub_assemblies: list[UUID] = []
    """List of sub-assembly job IDs, if any. Links to another ManufacturingJob."""

    # # These fields  will change based on the current conditions.
    # system_cost_index: EAM.SystemCostIndex
    # materials_adjusted_prices: MaterialsPriceProfile
    # materials_market_prices: MaterialsPriceProfile

    # This field depends on the blueprint, and location.
    materials_required: JobMaterials
    """The materials required for the job, keyed by type_id. Does not include sub-assemblies."""

    # This field depends on blueprint, location, system_cost_index, and materials_adjusted_prices fields.
    costs: ManufacturingJobCosts
    """The costs associated with the job, including EIV, facility tax, alpha tax, and SCC tax."""

    # This field depends on the blueprint, location, and character fields.
    build_time: int = -1
    """The build time in seconds, -1 if not calculated yet."""

    product: dict[int, int] = {}
    """The product produced by the job, keyed by type_id and quantity."""


class ResearchJob(BaseModel):
    """A Research job."""

    job_id: UUID
    notes: str = ""
    blueprint: JobBlueprint
    location: UUID
    """Location profile where the job is executed."""
    structure: UUID
    """Structure profile used for the job, e.g. a citadel or NPC station."""
    character: UUID
    """Character profile used for the job, e.g. skills and implants."""

    # # These fields will change based on the current conditions.
    # system_cost_index: EAM.SystemCostIndex
    # materials_adjusted_prices: MaterialsPriceProfile
    # materials_market_prices: MaterialsPriceProfile

    # This field depends on the blueprint.
    materials_required: JobMaterials
    """The materials required for the job, keyed by type_id. Does not include sub-assemblies."""

    # This field depends on blueprint, location, system_cost_index, and materials_adjusted_prices fields.
    costs: ResearchJobCosts
    """The costs associated with the job, including EIV, facility tax, alpha tax, and SCC tax."""

    # This field depends on the blueprint, location, and character fields.
    build_time: int = -1
    """The build time in seconds, -1 if not calculated yet."""


class CopyJob(BaseModel):
    """A Copy job."""

    job_id: UUID
    notes: str = ""
    blueprint: JobBlueprint
    location: UUID
    """Location profile where the job is executed."""
    structure: UUID
    """Structure profile used for the job, e.g. a citadel or NPC station."""
    character: UUID
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


class InventionJob(BaseModel):
    """An Invention job."""

    job_id: UUID
    notes: str = ""
    blueprint: JobBlueprint
    location: UUID
    """Location profile where the job is executed."""
    structure: UUID
    """Structure profile used for the job, e.g. a citadel or NPC station."""
    character: UUID
    """Character profile used for the job, e.g. skills and implants."""

    # # These fields will change based on the current conditions.
    # system_cost_index: EAM.SystemCostIndex
    # materials_adjusted_prices: MaterialsPriceProfile
    # materials_market_prices: MaterialsPriceProfile

    # This field depends on the blueprint.
    materials_required: JobMaterials
    """The materials required for the job, keyed by type_id. Does not include sub-assemblies."""

    # This field depends on blueprint, location, system_cost_index, and materials_adjusted_prices fields.
    costs: InventionJobCosts
    """The costs associated with the job, including EIV, facility tax, alpha tax, and SCC tax."""

    # This field depends on the blueprint, location, and character fields.
    build_time: int = -1
    """The build time in seconds, -1 if not calculated yet."""


class ReactionJob(BaseModel):
    """A Reaction job."""

    pass  # Placeholder for future fields


class IndustryJobAudit(BaseModel):
    """This is the top level model for a set of industry jobs."""

    character_profiles: dict[UUID, CharacterProfile]
    structure_profiles: dict[UUID, StructureProfile]
    location_profiles: dict[UUID, LocationProfile]
    manufacturing_jobs: dict[UUID, ManufacturingJob]
    research_jobs: dict[UUID, ResearchJob]
    copy_jobs: dict[UUID, CopyJob]
    invention_jobs: dict[UUID, InventionJob]
    reaction_jobs: dict[UUID, ReactionJob]

    # This is all "live" data that can change based on the current conditions.
    adjusted_prices: MaterialsPriceProfile
    materials_prices: MaterialsPriceProfile
    system_cost_indices: dict[int, dict[str, float]] = {}
