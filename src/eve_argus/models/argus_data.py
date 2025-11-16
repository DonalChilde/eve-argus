"""Models for the Argus app."""

from pydantic import BaseModel

from eve_argus.calculations.sde_queries import (
    get_market_path_int,
    get_market_path_string,
)

from . import static_data as SD
from .helpers import BaseModelToDisk


class MarketGroupArgus(BaseModel):
    """Model for a market group in the SDE."""

    _key: int
    description: str
    hasTypes: bool
    iconID: int | None
    name: str
    parentGroupID: int | None
    market_path_string: str | None = None
    market_path_int: list[int] | None = None


class MarketGroupsArgus(BaseModelToDisk):
    """Model for a collection of market groups in the SDE."""

    data: dict[int, MarketGroupArgus]
    info: SD.SdeInfo

    @classmethod
    def from_static_data(cls, static_data: SD.MarketGroups) -> "MarketGroupsArgus":
        """Create a MarketGroups model from the static data MarketGroups model."""
        result = cls(data={}, info=static_data.info)
        for mg_id, mg in static_data.data.items():
            market_path_int = get_market_path_int(mg_id, static_data)
            market_path_string = get_market_path_string(market_path_int, static_data)
            result.data[mg_id] = MarketGroupArgus(
                _key=mg._key,
                description=mg.description,
                hasTypes=mg.hasTypes,
                iconID=mg.iconID,
                name=mg.name,
                parentGroupID=mg.parentGroupID,
                market_path_int=market_path_int,
                market_path_string=market_path_string,
            )
        return result


# class ArgusType(BaseModel):
#     """Model for an Eve type in the Argus app."""

#     ...


# class ArgusTypes(BaseModelToDisk):
#     """Model for a collection of Eve types in the Argus app."""

#     data: dict[int, ArgusType]
#     info: SD.SdeInfo

#     @classmethod
#     def from_static_data(cls, static_data: SD.EveTypes) -> "ArgusTypes":
#         """Create an ArgusTypes model from the static data EveTypes model."""
#         ...

# class MarketType(BaseModel):
#     """Model for a market type in the Argus app."""

#     ...
