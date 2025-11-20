"""Models derived from data from the EVE Esi."""

from datetime import date
from enum import Enum
from typing import Any, Literal, Self

from esi_link.models import EsiResponse
from pydantic import BaseModel
from whenever import Instant

from .helpers import BaseModelToDisk

# Use type aliases for better readability IN TYPE HINTS.
type RegionId = int
type TypeId = int
type Period = int  # TODO: consider using Days for name clarity
type SolarSystemId = int
type CharacterId = int
type CorporationId = int
type AllianceId = int
type LocationId = int


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
    def from_json(cls, data: dict[str, Any]) -> Self:
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
    def from_esi_response(cls, response: EsiResponse) -> Self:
        """Create a MarketHistory instance from an ESI API response.

        operation_id: GetMarketsRegionIdHistory

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

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        """Create a SystemCostIndexDetail instance from JSON data.

        Args:
            data: A dictionary containing system cost index data with the following keys:
                - system_id: The solar system ID
                - copying: The copying cost index
                - duplicating: The duplicating cost index
                - invention: The invention cost index
                - manufacturing: The manufacturing cost index
                - reaction: The reaction cost index
                - researching_material_efficiency: The research material efficiency cost index
                - researching_technology: The research technology cost index
                - researching_time_efficiency: The research time efficiency cost index
                - reverse_engineering: The reverse engineering cost index
        """
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
        for value in data.get("cost_indices", []):
            values.update(value)
        values.update(data)
        return cls(system_id=data["solar_system_id"], **values)


class SystemCostIndices(SourcedFromESI):
    """System cost index model."""

    data: dict[SolarSystemId, SystemCostIndexDetail]
    """The system cost index details keyed by system ID."""

    @classmethod
    def from_esi_response(cls, response: EsiResponse) -> Self:
        """Create a SystemCostIndices instance from an ESI API response.

        operation_id: GetIndustrySystems
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
            detail = SystemCostIndexDetail.from_json(item)
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

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        """Create a UniverseMarketPriceDetail instance from JSON data.

        Args:
            data: A dictionary containing universe market price data with the following keys:
                - type_id: The type ID of the item
                - adjusted_price: The adjusted price of the item
                - average_price: The average price of the item
        """
        return cls(
            type_id=data["type_id"],
            adjusted_price=data["adjusted_price"],
            average_price=data["average_price"],
        )


class UniverseMarketPrices(SourcedFromESI):
    """A collection of universe pricing."""

    data: dict[TypeId, UniverseMarketPriceDetail]
    """A dictionary mapping type IDs to adjusted and average market prices for the universe."""

    @classmethod
    def from_esi_response(cls, response: EsiResponse) -> Self:
        """Create a UniverseMarketPrices instance from an ESI API response.

        operation_id: GetMarketsPrices
        Args:
            response (EsiResponse): The ESI API response containing universe market prices data.
                Must include an http_response with json_data.

        Returns:
            UniverseMarketPrices: A new UniverseMarketPrices instance populated with data from the
                ESI response, including metadata (last_modified, expires, retrieved)
                and universe market price details.

        Raises:
            ValueError: If the response has no HTTP response.
        """
        if response.http_response is None:
            raise ValueError(
                "No HTTP response in ESI response to create UniverseMarketPrices"
            )
        metadata = get_source_info_from_esi_response(response)
        data: dict[TypeId, UniverseMarketPriceDetail] = {}
        for item in response.http_response.json_data:
            detail = UniverseMarketPriceDetail.from_json(item)
            data[detail.type_id] = detail
        result = cls(
            last_modified=metadata["last_modified"],
            expires=metadata["expires"],
            retrieved=metadata["retrieved"],
            data=data,
        )
        return result


class RegionalMarketTypes(SourcedFromESI):
    """A list of type IDs that have active orders in the region, for efficient market indexing."""

    region_id: RegionId
    """The region ID for which the market types are listed."""
    type_ids: set[TypeId]
    """A set of type IDs available in the specified region."""

    @classmethod
    def from_esi_response(cls, response: EsiResponse) -> Self:
        """Create a RegionalMarketTypes instance from an ESI API response.

        operation_id: GetMarketsRegionIdTypes

        Args:
            response (EsiResponse): The ESI API response containing regional market types data.
                Must include an http_response with json_data and request parameters for region_id.

        Returns:
            RegionalMarketTypes: A new RegionalMarketTypes instance populated with data from the
                ESI response, including metadata (last_modified, expires, retrieved)
                and the list of type IDs.

        Raises:
            ValueError: If the response has no HTTP response or if region_id is missing from the request parameters.
        """
        if response.http_response is None:
            raise ValueError(
                "No HTTP response in ESI response to create RegionalMarketTypes"
            )
        region_id = response.request.path_parameters.get("region_id", None)
        metadata = get_source_info_from_esi_response(response)

        if region_id is None:
            msg = f"Missing region_id {region_id} in ESI response to create RegionalMarketTypes"
            raise ValueError(msg)

        type_ids = {int(type_id) for type_id in response.http_response.json_data}

        result = cls(
            last_modified=metadata["last_modified"],
            expires=metadata["expires"],
            retrieved=metadata["retrieved"],
            region_id=int(region_id),
            type_ids=type_ids,
        )
        return result


class MarketOrderDetail(BaseModel):
    order_id: int
    type_id: TypeId
    location_id: LocationId
    volume_total: int
    volume_remain: int
    min_volume: int
    price: float
    is_buy_order: bool
    issued: Instant
    duration: int
    range: str
    system_id: SolarSystemId

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        """Create a MarketOrderDetail instance from JSON data.

        Args:
            data: A dictionary containing market order data with the following keys:
                - order_id: The unique identifier for the market order
                - type_id: The type ID of the item being bought or sold
                - location_id: The location ID where the order is placed
                - volume_total: The total volume of items in the order
                - volume_remain: The remaining volume of items in the order
                - min_volume: The minimum volume required to fulfill the order
                - price: The price per unit for the order
                - is_buy_order: A boolean indicating if the order is a buy order
                - issued: The timestamp when the order was issued
                - duration: The duration of the order in days
                - range: The range of the order (e.g., "region", "solarsystem")
                - system_id: The solar system ID where the order is located

        Returns:
            MarketOrderDetail: A new MarketOrderDetail instance populated with data from the JSON dictionary.
        """
        return cls(
            order_id=data["order_id"],
            type_id=data["type_id"],
            location_id=data["location_id"],
            volume_total=data["volume_total"],
            volume_remain=data["volume_remain"],
            min_volume=data["min_volume"],
            price=data["price"],
            is_buy_order=data["is_buy_order"],
            issued=Instant.parse_iso(data["issued"]),
            duration=data["duration"],
            range=data["range"],
            system_id=data["system_id"],
        )


class MarketOrders(BaseModel):
    """A collection of orders for a specific type ID in a region."""

    region_id: RegionId
    type_id: TypeId
    buy_orders: list[MarketOrderDetail]
    sell_orders: list[MarketOrderDetail]

    def filter_orders(
        self,
        is_buy_order: bool | None = None,
        location_id: int | None = None,
        location_spec: Literal["region", "system", "station"] = "region",
    ) -> list[MarketOrderDetail]:
        """Filter orders by is_buy_order.

        Args:
            is_buy_order (bool | None): If True, return only buy orders. If False, return only sell orders.
                If None, return all orders.
            location_id (int | None): The location ID to filter by. If None, do not filter by location.
            location_spec (Literal["region", "system", "station"]): The location specification to filter by.
                Defaults to "region".

        Returns:
            list[MarketOrderDetail]: The filtered list of market orders.
        """
        filtered_orders = []
        match is_buy_order:
            case True:
                filtered_orders = list(self.buy_orders)
            case False:
                filtered_orders = list(self.sell_orders)
            case None:
                filtered_orders = self.buy_orders + self.sell_orders
        if location_id is not None:
            match location_spec:
                case "region":
                    pass  # No filtering needed for region
                case "system":
                    filtered_orders = [
                        order
                        for order in filtered_orders
                        if order.system_id == location_id
                    ]
                case "station":
                    filtered_orders = [
                        order
                        for order in filtered_orders
                        if order.location_id == location_id
                    ]
                case _:
                    msg = (
                        f"Invalid location_spec: {location_spec}, do not filter by "
                        f"location_id. Did you give an id without a spec?"
                    )
                    raise ValueError(msg)
        return filtered_orders


class RegionalMarketOrders(SourcedFromESI):
    """A collection of market orders in a region.

    operation_id: GetMarketsRegionIdOrders
    """

    region_id: RegionId
    data: dict[TypeId, MarketOrders]

    @classmethod
    def from_esi_response(cls, response: EsiResponse) -> Self:
        """Create a RegionalMarketOrders instance from an ESI API response.

        Args:
            response (EsiResponse): The ESI API response containing regional market orders data.
                Must include an http_response with json_data and request parameters for region_id.

        Returns:
            RegionalMarketOrders: A new RegionalMarketOrders instance populated with data from the
                ESI response, including metadata (last_modified, expires, retrieved)
                and the list of market orders.

        Raises:
            ValueError: If the response has no HTTP response or if region_id is missing from the
                request parameters.
        """
        if response.http_response is None:
            raise ValueError(
                "No HTTP response in ESI response to create RegionalMarketOrders"
            )
        region_id = response.request.path_parameters.get("region_id", None)
        metadata = get_source_info_from_esi_response(response)

        if region_id is None:
            msg = f"Missing region_id {region_id} in ESI response to create RegionalMarketOrders"
            raise ValueError(msg)

        data: dict[TypeId, MarketOrders] = {}
        for item in response.http_response.json_data:
            detail = MarketOrderDetail.from_json(item)
            if detail.type_id in data:
                orders = data[detail.type_id]
                if detail.is_buy_order:
                    orders.buy_orders.append(detail)
                else:
                    orders.sell_orders.append(detail)
            else:
                orders = MarketOrders(
                    region_id=int(region_id),
                    type_id=detail.type_id,
                    buy_orders=[detail] if detail.is_buy_order else [],
                    sell_orders=[detail] if not detail.is_buy_order else [],
                )
            data[detail.type_id] = orders

        result = cls(
            last_modified=metadata["last_modified"],
            expires=metadata["expires"],
            retrieved=metadata["retrieved"],
            region_id=int(region_id),
            data=data,
        )
        return result
