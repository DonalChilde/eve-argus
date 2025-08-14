import pytest

from eve_argus.argus_esi.argus_esi import ArgusEsi
from eve_argus.eve_argus_esi.esi_cache.esi_memory_cache import EsiMemoryCache
from eve_argus.eve_argus_esi.esi_client.argus_aiohttp.esi_client import (
    ArgusAiohttpClient,
)
from eve_argus.eve_argus_esi.esi_client.esi_client_protocol import EsiClientProtocol
from eve_argus.eve_argus_esi.esi_schema.eve_openapi import EveOpenApi


@pytest.fixture(scope="module", name="esi_cache")
def esi_cache_():
    return EsiMemoryCache()


@pytest.fixture(scope="module", name="eve_openapi")
def eve_openapi_(esi_schema):
    return EveOpenApi(spec=esi_schema)


@pytest.fixture(scope="module", name="esi_client")
def esi_client_(eve_openapi, esi_cache) -> EsiClientProtocol:
    esi_client = ArgusAiohttpClient(
        cache=esi_cache,
        api_spec=eve_openapi,
        base_url="https://esi.evetech.net/latest",
        user_agent_prefix="Eve Argus testing",
    )
    return esi_client


@pytest.fixture(scope="module", name="argus_esi")
def argus_esi_(esi_client) -> ArgusEsi:
    return ArgusEsi(esi_client=esi_client)


def test_market_history(argus_esi: ArgusEsi):
    region_id = 10000002  # The Forge
    type_id = 34  # Tritanium
    market_history = argus_esi.market_history(region_id, type_id)
    print(f"{market_history!r}")
    assert market_history is not None
    assert market_history.region_id == region_id
    assert market_history.type_id == type_id
    assert market_history.last_modified is not None
    assert market_history.expires is not None
    assert market_history.etag is not None
    assert len(market_history.data) > 0
