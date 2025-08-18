"""Transform ESI data models to Argus data models."""

import json
import logging
from typing import TypedDict
from uuid import UUID, uuid4

from eve_argus.eve_argus_esi.esi_models import EsiAction, EsiResponse
from eve_argus.models import argus as EAM

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# def market_prices_universe(
#     action: EsiAction,
# ) -> EAM.UniverseMarketPrices:
#     """Import market prices for the universe from a sequence of dictionaries."""
#     cache_fields = get_cache_fields(action.response)
#     result = EAM.UniverseMarketPrices(
#         **cache_fields,
#         data_set_id=uuid4(),
#         data_type=EAM.DataTypes.UniverseMarketPrices,
#         description="Universe market prices",
#         data_source=None,
#         data={},
#     )
#     if action.response is None or action.response.data is None:
#         return result
#     for item in action.response.data:
#         prices = EAM.UniverseMarketPrice(
#             type_id=item["type_id"],
#             adjusted_price=item["adjusted_price"],
#             average_price=item.get("average_price", -1.0),
#         )
#         result.data[item["type_id"]] = prices
#     return result
def _validate_action(action: EsiAction) -> None:
    if action.response is None or not action.response.text:
        logger.error(
            "EsiResponse is None or empty, cannot process. %r",
            action,
        )
        raise ValueError("EsiResponse is None or empty, cannot process.")


class ExtractedMetadata(TypedDict):
    expires: str
    """The expiration time for the cache key in ISO 8601 format."""
    etag: str
    """The ETag for the cached response."""
    last_modified: str
    """The last modified time for the cached response in ISO 8601 format."""
    last_checked: str
    """The last time this ESI route was checked in ISO 8601 format."""
    data_source: UUID | None


def extract_metadata(action: EsiAction) -> ExtractedMetadata:
    """Get the values from the EsiAction cache metadata.

    Use cache key as data_source, then pop out the key.
    """
    if action.cache_metadata is None:
        return {}  # type: ignore
    metadata = action.cache_metadata
    result: ExtractedMetadata = {
        "expires": metadata.expires,
        "etag": metadata.etag,
        "last_modified": metadata.last_modified,
        "last_checked": metadata.last_checked,
        "data_source": metadata.key,
    }
    return result


def market_prices(action: EsiAction) -> EAM.UniverseMarketPrices:
    """Import adjusted and average market prices for the Eve universe from esi response.

    ```python
    response_schema = {
        "MarketsPricesGet": {
            "items": {
                "properties": {
                    "adjusted_price": {"format": "double", "type": "number"},
                    "average_price": {"format": "double", "type": "number"},
                    "type_id": {"format": "int64", "type": "integer"},
                },
                "required": ["type_id"],
                "type": "object",
            },
            "type": "array",
        }
    }
    ```
    """
    _validate_action(action)
    meta_dict = extract_metadata(action)
    result = EAM.UniverseMarketPrices(
        **meta_dict,
        data_set_id=uuid4(),
        description="Adjusted and average market prices for the Eve universe",
        data={},
    )
    json_data = json.loads(action.response.text[0] if action.response else "[]")
    for item in json_data:
        prices = EAM.UniverseMarketPrice(
            type_id=item["type_id"],
            adjusted_price=item["adjusted_price"],
            average_price=item.get("average_price", -1.0),
        )
        result.data[item["type_id"]] = prices
    return result


def market_history(
    action: EsiAction,
) -> EAM.MarketHistory:
    """Import market history for a specific region and type from esi response.

        ```python
        response_schema = {
        "MarketsRegionIdHistoryGet": {
            "items": {
                "properties": {
                    "average": {"format": "double", "type": "number"},
                    "date": {
                        "description": "The date of this historical statistic entry",
                        "format": "date",
                        "type": "string",
                    },
                    "highest": {"format": "double", "type": "number"},
                    "lowest": {"format": "double", "type": "number"},
                    "order_count": {
                        "description": "Total number of orders happened that day",
                        "format": "int64",
                        "type": "integer",
                    },
                    "volume": {
                        "description": "Total",
                        "format": "int64",
                        "type": "integer",
                    },
                },
                "required": [
                    "date",
                    "order_count",
                    "volume",
                    "highest",
                    "average",
                    "lowest",
                ],
                "type": "object",
            },
            "type": "array",
        }
    }
        ```
    """
    _validate_action(action)
    meta_dict = extract_metadata(action)
    region_id = int(action.request.path_params["region_id"])
    type_id = int(action.request.query_params["type_id"])
    data: list[EAM.MarketHistoryDetail] = []
    json_data = json.loads(action.response.text[0] if action.response else "[]")
    for item in json_data:
        data.append(
            EAM.MarketHistoryDetail(region_id=region_id, type_id=type_id, **item)
        )

    history = EAM.MarketHistory(
        **meta_dict,
        data_set_id=uuid4(),
        description=f"Market history for region {region_id} and type {type_id}",
        region_id=region_id,
        type_id=type_id,
        data=data,
    )
    return history


def market_orders(action: EsiAction) -> EAM.RegionalMarketOrders:
    """Import market orders for a specific region from esi response.

    ```python
    response_schema = {
        "MarketsRegionIdOrdersGet": {
            "items": {
                "properties": {
                    "duration": {"format": "int64", "type": "integer"},
                    "is_buy_order": {"type": "boolean"},
                    "issued": {"format": "date-time", "type": "string"},
                    "location_id": {"format": "int64", "type": "integer"},
                    "min_volume": {"format": "int64", "type": "integer"},
                    "order_id": {"format": "int64", "type": "integer"},
                    "price": {"format": "double", "type": "number"},
                    "range": {
                        "enum": [
                            "station",
                            "region",
                            "solarsystem",
                            "1",
                            "2",
                            "3",
                            "4",
                            "5",
                            "10",
                            "20",
                            "30",
                            "40",
                        ],
                        "type": "string",
                    },
                    "system_id": {
                        "description": "The solar system this order was placed",
                        "format": "int64",
                        "type": "integer",
                    },
                    "type_id": {"format": "int64", "type": "integer"},
                    "volume_remain": {"format": "int64", "type": "integer"},
                    "volume_total": {"format": "int64", "type": "integer"},
                },
                "required": [
                    "order_id",
                    "type_id",
                    "location_id",
                    "system_id",
                    "volume_total",
                    "volume_remain",
                    "min_volume",
                    "price",
                    "is_buy_order",
                    "duration",
                    "issued",
                    "range",
                ],
                "type": "object",
            },
            "type": "array",
        }
    }
    ```
    """
    _validate_action(action)
    meta_dict = extract_metadata(action)
    if "type_id" in action.request.query_params:
        raise ValueError(
            "Market orders for a specific type are not supported in this function."
        )
    response = action.response
    region_id = int(action.request.path_params["region_id"])
    result = EAM.RegionalMarketOrders(
        **meta_dict,
        data_set_id=uuid4(),
        description=f"Market orders for region {region_id}",
        region_id=region_id,
        orders={},
    )

    for text_line in response.text if response else []:
        json_orders = json.loads(text_line)
        for json_order in json_orders:
            order = EAM.MarketOrderDetail(region_id=region_id, **json_order)
            if order.type_id not in result.orders:
                result.orders[order.type_id] = EAM.MarketOrders(
                    region_id=region_id, type_id=order.type_id
                )
            if order.is_buy_order:
                result.orders[order.type_id].buy_orders.append(order)
            else:
                result.orders[order.type_id].sell_orders.append(order)

    return result


def system_cost_indices(action: EsiAction) -> EAM.SystemCostIndices:
    """Import system cost indices from esi response.

    ```python
    response_schema = {
        "GetIndustrySystems": {
            "items": {
                "properties": {
                    "cost_indices": {
                        "items": {
                            "description": "cost_indice object",
                            "properties": {
                                "activity": {
                                    "enum": [
                                        "copying",
                                        "duplicating",
                                        "invention",
                                        "manufacturing",
                                        "none",
                                        "reaction",
                                        "researching_material_efficiency",
                                        "researching_technology",
                                        "researching_time_efficiency",
                                        "reverse_engineering",
                                    ],
                                    "type": "string",
                                },
                                "cost_index": {"format": "double", "type": "number"},
                            },
                            "required": ["activity", "cost_index"],
                            "type": "object",
                        },
                        "type": "array",
                    },
                    "solar_system_id": {"format": "int64", "type": "integer"},
                },
                "required": ["solar_system_id", "cost_indices"],
                "type": "object",
            },
            "type": "array",
        }
    }
    ```
    """
    _validate_action(action)
    meta_dict = extract_metadata(action)
    response = action.response
    result = EAM.SystemCostIndices(
        **meta_dict,
        data_set_id=uuid4(),
        description="System cost indices for manufacturing, research, and reactions",
        data={},
    )
    json_data = json.loads(response.text[0] if response else "{}")
    for sci in json_data:
        system_id = sci["solar_system_id"]
        result.data[system_id] = EAM.SystemCostIndex(system_id=system_id, **sci)
    return result


# def region_market_types_from_esi(
#     region_id: int,
#     action: EsiAction,
# ) -> EAM.RegionalMarketTypes:
#     """Import region market types from a sequence of integers."""
#     cache_fields = get_cache_fields(action.response)
#     result = EAM.RegionalMarketTypes(
#         **cache_fields,
#         data_set_id=uuid4(),
#         data_type=EAM.DataTypes.RegionalMarketTypes,
#         description="Region market types",
#         data_source=None,
#         region_id=region_id,
#         type_ids=set(),
#     )
#     if action.response is None or action.response.data is None:
#         return result
#     # collect the lists of type IDs from the action response and its pages
#     type_lists: list[list[int]] = [
#         action.response.data if action.response and action.response.data else [],
#         *[page.response.data for page in action.pages if page.response],
#     ]
#     # Flatten the list of lists into a single list of type IDs
#     flat_data: list[int] = list(chain(*type_lists))
#     result.type_ids.update(flat_data)
#     return result


# def region_market_orders_from_esi(
#     region_id: int,
#     action: EsiAction,
# ) -> EAM.RegionalMarketOrders:
#     """Import market orders for a specific region from a sequence of dictionaries."""
#     cache_fields = get_cache_fields(action.response)
#     result = EAM.RegionalMarketOrders(
#         **cache_fields,
#         data_set_id=uuid4(),
#         data_type=EAM.DataTypes.RegionalMarketOrders,
#         description=f"Regional market orders for {region_id}",
#         data_source=None,
#         region_id=region_id,
#         orders={},
#     )
#     orders = [
#         action.response.data if action.response and action.response.data else [],
#         *[page.response.data for page in action.pages if page.response],
#     ]
#     flattened_data = chain(*orders)
#     for esi_order in flattened_data:
#         argus_order = EAM.MarketOrderDetail(region_id=region_id, **esi_order)
#         if argus_order.type_id not in result.orders:
#             result.orders[argus_order.type_id] = EAM.MarketOrders(
#                 region_id=region_id, type_id=argus_order.type_id
#             )
#         if argus_order.is_buy_order:
#             result.orders[argus_order.type_id].buy_orders.append(argus_order)
#         else:
#             result.orders[argus_order.type_id].sell_orders.append(argus_order)
#     return result


# def system_cost_indices_from_esi(
#     action: EsiAction,
# ) -> EAM.SystemCostIndices:
#     """Import system cost indices from a sequence of dictionaries."""
#     cache_fields = get_cache_fields(action.response)
#     result = EAM.SystemCostIndices(
#         **cache_fields,
#         data_set_id=uuid4(),
#         data_type=EAM.DataTypes.SystemCostIndices,
#         description="System cost indices",
#         data_source=None,
#         data={},
#     )
#     if action.response is None or action.response.data is None:
#         return result
#     for item in action.response.data:
#         system_id = item["solar_system_id"]
#         result.data[system_id] = EAM.SystemCostIndex(
#             system_id=system_id,
#             manufacturing=item["manufacturing"],
#             research_material=item["researching_material_efficiency"],
#             research_time=item["researching_time_efficiency"],
#             copying=item["copying"],
#             invention=item["invention"],
#             reaction=item["reaction"],
#         )
#     return result
