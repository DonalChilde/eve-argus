"""Top level api to get data from ESI using an Argus ESI client."""

import logging
from collections.abc import Sequence
from datetime import UTC, datetime

from eve_argus.argus_esi import esi_to_argus as DI
from eve_argus.argus_esi import request_builder as RB
from eve_argus.eve_argus_esi.esi_client.esi_client_protocol import EsiClientProtocol
from eve_argus.eve_argus_esi.esi_models import EsiAction
from eve_argus.models import argus as EAM

logger = logging.getLogger(__name__)

## Cache thoughts.
# - ESI responses include an ETag header for caching.
# - If the client has a cached response with the same ETag, it can use that instead of making a new request.
# - The client should handle ETag matching and caching logic.
# - The ESI response also offer an expires field that can be used to determine when to invalidate the cache.
# - The expires field can be checked locally, but the etag field must be checked with the server.


def is_expired(obj: EAM.TopLevelDataSet) -> bool:
    """Check to see if the Argus dataset is expired."""
    if obj.expires:
        return datetime.fromisoformat(obj.expires).astimezone(UTC) < datetime.now(UTC)
    return False


def regional_market_history(
    esi_client: EsiClientProtocol,
    region_id: int,
    type_ids: Sequence[int],
    description: str = "",
    cache_results=True,
    override_cached=False,
) -> EAM.RegionalMarketHistory:
    """Get market histories for a specific region, and multiple types."""
    requests = RB.market_history_batch(region_id, type_ids)
    actions = [EsiAction(request=x) for x in requests]
    esi_client.get_ops(
        actions=actions, cache_results=cache_results, override_cached=override_cached
    )
    result = EAM.RegionalMarketHistory(
        region_id=region_id, description=description, data={}
    )
    for action in actions:
        history = DI.market_history(action)
        result.data[history.type_id] = history
    return result


def market_history(
    esi_client: EsiClientProtocol,
    region_id: int,
    type_id: int,
    etag: str = "",
    cache_results=True,
    override_cached=False,
) -> EAM.MarketHistory:
    """Get market history for a specific region and type."""
    action = EsiAction(request=RB.market_history(region_id, type_id, etag))
    # TODO handle etag match signal from esi_client
    esi_client.get_op(
        action, cache_results=cache_results, override_cached=override_cached
    )
    return DI.market_history(action)


def market_prices(
    esi_client: EsiClientProtocol,
    etag: str = "",
    cache_results=True,
    override_cached=False,
) -> EAM.UniverseMarketPrices:
    """Get market prices for the entire universe."""
    action = EsiAction(request=RB.market_prices(etag))
    esi_client.get_op(
        action, cache_results=cache_results, override_cached=override_cached
    )
    return DI.market_prices(action)


def market_orders(
    esi_client: EsiClientProtocol,
    region_id: int,
    etag: str = "",
    cache_results=True,
    override_cached=False,
) -> EAM.RegionalMarketOrders:
    """Get market orders for a specific region."""
    action = EsiAction(request=RB.market_orders(region_id, etag))
    esi_client.get_op(
        action, cache_results=cache_results, override_cached=override_cached
    )
    return DI.market_orders(action)


def system_cost_indices(
    esi_client: EsiClientProtocol,
    etag: str = "",
    cache_results=True,
    override_cached=False,
) -> EAM.SystemCostIndices:
    """Get system cost indices for the Eve universe."""
    action = EsiAction(request=RB.system_cost_indices(etag))
    esi_client.get_op(
        action, cache_results=cache_results, override_cached=override_cached
    )
    return DI.system_cost_indices(action)
