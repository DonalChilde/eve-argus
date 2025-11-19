"""Models derived from data from the EVE Esi."""

from datetime import date
from enum import Enum
from typing import Any

from esi_link.models import EsiResponse
from pydantic import BaseModel
from whenever import Instant

from .helpers import BaseModelToDisk

# Use type aliases for better readability IN TYPE HINTS.
type RegionId = int
type TypeId = int
type Period = int
type SolarSystemId = int


class Activity_Name(Enum):
    """Enum for activity names in Eve Argus.

    Keep this data, not sure where is offical source is.
    Found this on fuzzworks.
    """

    manufacturing = 1
    research_time = 3
    research_material = 4
    copying = 5
    invention = 8
    reaction = 11


def get_source_info_from_esi_response(response: EsiResponse) -> dict[str, Instant]:
    """Extract source info from an ESI response."""
    if response.http_response is None:
        raise ValueError("No HTTP response in ESI response to extract source info")
    return {
        "last_modified": Instant.parse_rfc2822(response.http_response.last_modified),
        "expires": Instant.parse_rfc2822(response.http_response.expires),
        "retrieved": response.http_response.completed_on,
    }


class SourcedFromESI(BaseModelToDisk):
    """Base model for data sourced from ESI.

    Typically used to represent an atomic request/response pair from ESI,
    not aggregations of multiple requests/responses.
    """

    last_modified: Instant
    expires: Instant
    retrieved: Instant


class MarketHistoryDetail(BaseModel):
    average: float
    date: date
    highest: float
    lowest: float
    order_count: int
    volume: int

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "MarketHistoryDetail":
        """Create a MarketHistoryDetail instance from JSON data.

        Args:
            data: A dictionary containing market history data with the following keys:
                - average: The average price for the day
                - date: The date in ISO format (YYYY-MM-DD)
                - highest: The highest price for the day
                - lowest: The lowest price for the day
                - order_count: The number of orders for the day
                - volume: The total volume traded for the day

        Returns:
            MarketHistoryDetail: A new instance populated with the provided data

        Raises:
            KeyError: If any required key is missing from the data dictionary
            ValueError: If the date string is not in valid ISO format
        """
        return cls(
            average=data["average"],
            date=date.fromisoformat(data["date"]),
            highest=data["highest"],
            lowest=data["lowest"],
            order_count=data["order_count"],
            volume=data["volume"],
        )


class MarketHistory(SourcedFromESI):
    region_id: RegionId
    type_id: TypeId
    data: dict[date, MarketHistoryDetail]

    @classmethod
    def from_esi_response(cls, response: EsiResponse) -> "MarketHistory":
        """Create a MarketHistory instance from an ESI API response.

        Args:
            response (EsiResponse): The ESI API response containing market history data.
                Must include an http_response with json_data, and request parameters
                for region_id and type_id.

        Returns:
            MarketHistory: A new MarketHistory instance populated with data from the
                ESI response, including metadata (last_modified, expires, retrieved)
                and market history details.

        Raises:
            ValueError: If the response has no HTTP response, or if region_id or
                type_id are missing from the request parameters.
        """
        if response.http_response is None:
            raise ValueError("No HTTP response in ESI response to create MarketHistory")
        region_id = response.request.path_parameters.get("region_id", None)
        type_id = response.request.query_parameters.get("type_id", None)
        metadata = get_source_info_from_esi_response(response)

        if region_id is None or type_id is None:
            msg = f"Missing region_id {region_id} or type_id {type_id} in ESI response to create MarketHistory"
            raise ValueError(msg)
        data: dict[date, MarketHistoryDetail] = {}
        for item in response.http_response.json_data:
            detail = MarketHistoryDetail.from_json(item)
            data[detail.date] = detail
        sorted_by_date = sorted(data.items(), reverse=True)
        result = cls(
            last_modified=metadata["last_modified"],
            expires=metadata["expires"],
            retrieved=metadata["retrieved"],
            region_id=int(region_id),
            type_id=int(type_id),
            data=dict(sorted_by_date),
        )
        return result


class SystemCostIndexDetail(BaseModel):
    """System cost index data model."""

    system_id: int
    """The solar system ID."""
    copying: float
    """The copying cost index."""
    duplicating: float
    """The duplicating cost index."""
    invention: float
    """The invention cost index."""
    manufacturing: float
    """The manufacturing cost index."""
    reaction: float
    """The reaction cost index."""
    researching_material_efficiency: float
    """The research material efficiency cost index."""
    researching_technology: float
    """The research technology cost index."""
    researching_time_efficiency: float
    """The research time efficiency cost index."""
    reverse_engineering: float
    """The reverse engineering cost index."""


class SystemCostIndices(SourcedFromESI):
    """System cost index model."""

    data: dict[SolarSystemId, SystemCostIndexDetail]
    """The system cost index details keyed by system ID."""

    @classmethod
    def from_esi_response(cls, response: EsiResponse) -> "SystemCostIndices":
        """Create a SystemCostIndices instance from an ESI API response.

        The response data is in the form of dict[solar_system_id: int, cost_indices: list[dict[str, float]]].

        Args:
            response (EsiResponse): The ESI API response containing system cost index data.
                Must include an http_response with json_data.

        Returns:
            SystemCostIndex: A new SystemCostIndex instance populated with data from the
                ESI response, including metadata (last_modified, expires, retrieved)
                and system cost index details.

        Raises:
            ValueError: If the response has no HTTP response.
        """
        if response.http_response is None:
            raise ValueError(
                "No HTTP response in ESI response to create SystemCostIndex"
            )
        metadata = get_source_info_from_esi_response(response)
        data: dict[SolarSystemId, SystemCostIndexDetail] = {}
        for item in response.http_response.json_data:
            values = {
                "copying": 0.0,
                "duplicating": 0.0,
                "invention": 0.0,
                "manufacturing": 0.0,
                "reaction": 0.0,
                "researching_material_efficiency": 0.0,
                "researching_technology": 0.0,
                "researching_time_efficiency": 0.0,
                "reverse_engineering": 0.0,
            }
            for value in item.get("cost_indices", []):
                values.update(value)
            detail = SystemCostIndexDetail(system_id=item["solar_system_id"], **values)
            data[detail.system_id] = detail
        result = cls(
            last_modified=metadata["last_modified"],
            expires=metadata["expires"],
            retrieved=metadata["retrieved"],
            data=data,
        )
        return result


class UniverseMarketPriceDetail(BaseModel):
    """Universe Market prices data model."""

    type_id: int
    """The type ID of the item."""
    adjusted_price: float
    """The adjusted price of the item, -1.0 if not available."""
    average_price: float
    """The average price of the item, -1.0 if not available."""


class UniverseMarketPrices(SourcedFromESI):
    """A collection of universe pricing."""

    data: dict[TypeId, UniverseMarketPriceDetail]
    """A dictionary mapping type IDs to adjusted and average market prices for the universe."""
