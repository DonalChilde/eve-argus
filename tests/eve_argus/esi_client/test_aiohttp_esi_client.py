"""Tests for the aiohttp esi client."""

from uuid import uuid4

import pytest

from eve_argus.eve_argus_esi.esi_cache.esi_memory_cache import EsiMemoryCache
from eve_argus.eve_argus_esi.esi_client.argus_aiohttp.esi_client import (
    ArgusAiohttpClient,
)
from eve_argus.eve_argus_esi.esi_models import EsiAction, EsiRequest
from eve_argus.eve_argus_esi.esi_schema.eve_openapi import EveOpenApi
from eve_argus.helpers.cache_id_from_url import cache_id_from_url
from eve_argus.helpers.esi_cache_url import compile_cache_url


def test_get_operation(esi_schema):
    api_spec = EveOpenApi(spec=esi_schema)
    base_url = "https://esi.evetech.net/latest/"
    cache = EsiMemoryCache()
    esi_client = ArgusAiohttpClient(
        api_spec=api_spec,
        base_url=base_url,
        cache=cache,
        user_agent_prefix="Testing...",
    )
    op_id = "GetMarketsRegionIdHistory"
    path_params = {"region_id": 10000002}
    query_params = {"type_id": 34}

    action = EsiAction(
        request=EsiRequest(
            request_id=uuid4(),
            op_id=op_id,
            path_params=path_params,
            query_params=query_params,
            method="GET",
            # cache_key=test_cache_key,
        )
    )
    cache_url = compile_cache_url(
        base_url=esi_client.base_url,
        request=action.request,
        open_api=esi_client.api_spec,
    )
    test_cache_key = cache_id_from_url(cache_url)

    esi_client.get_op(action, cache_results=True, override_cached=False)
    assert action.response is not None
    assert action.response.request_id == action.request.request_id
    assert action.response.cache_key == test_cache_key
    assert len(action.response.text) == 1
    assert action.response.source == "api"

    esi_client.get_op(action, cache_results=True, override_cached=False)
    assert action.response.source == "cache"


@pytest.mark.slow
def test_get_paged_operation(esi_schema):
    api_spec = EveOpenApi(spec=esi_schema)
    base_url = "https://esi.evetech.net/latest/"
    cache = EsiMemoryCache()
    esi_client = ArgusAiohttpClient(
        api_spec=api_spec,
        base_url=base_url,
        cache=cache,
        user_agent_prefix="Testing...",
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
        )
    )
    cache_url = compile_cache_url(
        base_url=esi_client.base_url,
        request=action.request,
        open_api=esi_client.api_spec,
    )
    test_cache_key = cache_id_from_url(cache_url)
    esi_client.get_op(action, cache_results=True, override_cached=False)
    assert action.response is not None
    assert action.response.request_id == action.request.request_id
    assert action.response.cache_key == test_cache_key
    assert len(action.response.text) > 5
    assert action.response.source == "api"

    esi_client.get_op(action, cache_results=True, override_cached=False)
    assert action.response.source == "cache"
