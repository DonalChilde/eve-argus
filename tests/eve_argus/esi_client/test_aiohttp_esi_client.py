"""Tests for the aiohttp esi client."""

from uuid import uuid4

from eve_argus.esi_client.argus_aiohttp.esi_cache import EsiMemoryCache
from eve_argus.esi_client.argus_aiohttp.esi_client import ArgusAiohttpClient
from eve_argus.esi_client.eve_openapi import EveOpenApi
from eve_argus.models.esi import EsiAction, EsiRequest


def test_get_operation(esi_schema):
    api_spec = EveOpenApi(spec=esi_schema)
    base_url = "https://esi.evetech.net/latest/"
    cache = EsiMemoryCache()
    esi_client = ArgusAiohttpClient(
        api_spec=api_spec,
        base_url=base_url,
        cache=cache,
    )
    op_id = "GetMarketsRegionIdHistory"
    path_params = {"region_id": 10000002}
    query_params = {"type_id": 34}
    test_cache_key = uuid4()
    action = EsiAction(
        request=EsiRequest(
            request_id=uuid4(),
            op_id=op_id,
            path_params=path_params,
            query_params=query_params,
            method="GET",
            cache_key=test_cache_key,
        )
    )
    esi_client.get_op(action, cache_result=True, override_cached=False)
    assert action.response is not None
    assert action.response.request_id == action.request.request_id
    assert action.response.cache_key == test_cache_key
    assert len(action.response.text) == 1
    assert action.response.source == "api"

    esi_client.get_op(action, cache_result=True, override_cached=False)
    assert action.response.source == "cache"


def test_get_paged_operation(esi_schema):
    api_spec = EveOpenApi(spec=esi_schema)
    base_url = "https://esi.evetech.net/latest/"
    cache = EsiMemoryCache()
    esi_client = ArgusAiohttpClient(
        api_spec=api_spec,
        base_url=base_url,
        cache=cache,
    )
    op_id = "GetMarketsRegionIdOrders"
    path_params = {"region_id": 10000002}
    query_params = {"order_type": "all"}
    test_cache_key = uuid4()
    action = EsiAction(
        request=EsiRequest(
            request_id=uuid4(),
            op_id=op_id,
            path_params=path_params,
            query_params=query_params,
            method="GET",
            cache_key=test_cache_key,
        )
    )
    esi_client.get_op(action, cache_result=True, override_cached=False)
    assert action.response is not None
    assert action.response.request_id == action.request.request_id
    assert action.response.cache_key == test_cache_key
    assert len(action.response.text) > 5
    assert action.response.source == "api"

    esi_client.get_op(action, cache_result=True, override_cached=False)
    assert action.response.source == "cache"


#'Tue, 12 Aug 2025 11:05:00 GMT'
