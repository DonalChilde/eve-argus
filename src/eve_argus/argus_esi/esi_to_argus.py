"""Transform ESI data models to Argus data models."""

import json
import logging
from collections.abc import Sequence
from datetime import UTC, datetime
from itertools import chain
from typing import Any
from uuid import uuid4

from eve_argus.eve_argus_esi.esi_models import EsiAction
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


def market_history(
    action: EsiAction,
) -> EAM.MarketHistory:
    """Import market history for a specific region and type from esi response."""
    if action.response is None or not action.response.text:
        logger.error(
            "EsiAction response is None or empty, cannot process market history. %r",
            action,
        )
        raise ValueError(
            "EsiAction response is None or empty, cannot process market history."
        )
    region_id = int(action.request.path_params["region_id"])
    type_id = int(action.request.query_params["type_id"])
    data: list[EAM.MarketHistoryDetail] = []
    json_data = json.loads(action.response.text[0] if action.response else "[]")
    for item in json_data:
        data.append(
            EAM.MarketHistoryDetail(region_id=region_id, type_id=type_id, **item)
        )

    history = EAM.MarketHistory(
        data_set_id=uuid4(),
        data_type=EAM.DataTypes.MarketHistory,
        description=f"Market history for region {region_id} and type {type_id}",
        data_source=None,
        region_id=region_id,
        type_id=type_id,
        data=data,
        last_modified=action.response.last_modified,
        expires=action.response.expires,
        etag=action.response.etag,
    )
    return history


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
