"""Models derived from data from the EVE Esi."""

from datetime import date
from typing import Any

from esi_link.models import EsiResponse
from pydantic import BaseModel
from whenever import Instant

from .helpers import BaseModelToDisk

# Use type aliases for better readability IN TYPE HINTS.
type RegionId = int
type TypeId = int
type Period = int


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
    data: list[MarketHistoryDetail]

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

        data = [
            MarketHistoryDetail.from_json(item)
            for item in response.http_response.json_data
        ]
        result = cls(
            last_modified=metadata["last_modified"],
            expires=metadata["expires"],
            retrieved=metadata["retrieved"],
            region_id=int(region_id),
            type_id=int(type_id),
            data=data,
        )
        return result


class MarketHistorySummary(BaseModel):
    """Market history summary data model."""

    region_id: int
    type_id: int
    period: int
    start: str
    end: str
    missing: int
    highest: float
    average: float
    lowest: float
    order_count: int
    volume: float
    last_modified: str
    """The UTC datetime that is the last_modified of the source data, in ISO 8601 format."""


class MarketHistorySummmaries(BaseModelToDisk):
    """Collection of market history summaries."""

    # Consider the best way to collect these. There is also date to consider.
    data: dict[tuple[RegionId, TypeId, Period], MarketHistorySummary]
    # info: SD.SdeInfo
