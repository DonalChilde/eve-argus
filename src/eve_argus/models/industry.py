from collections.abc import Sequence
from math import ceil
from uuid import UUID, uuid4

from pydantic import BaseModel

from eve_argus.models import argus as EAM


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


class JobBlueprint(BaseModel):
    """Represents a blueprint used in a job."""

    type_id: int
    material_efficiency: int
    time_efficiency: int


class JobLocation(BaseModel):
    """Represents the location where a job is executed."""

    pass
