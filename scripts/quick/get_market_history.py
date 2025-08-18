# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

from pathlib import Path
from time import perf_counter

from eve_argus.argus_esi import argus_esi as FETCH
from eve_argus.eve_argus_esi.esi_cache.esi_memory_cache import EsiMemoryCache
from eve_argus.eve_argus_esi.esi_client.aiohttp_client import (
    ArgusAiohttpClient,
)
from eve_argus.eve_argus_esi.esi_schema.eve_openapi import EveOpenApi
from eve_argus.file_io.argus_data_file_reader import ArgusFileReader
from eve_argus.file_io.argus_data_file_writer import ArgusFileWriter
from eve_argus.models import argus as EAM
from eve_argus.models.argus import TypeIDSubsets

ARGUS_STATIC_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "static-data"
ARGUS_ESI_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "esi-data"
ARGUS_EXPORT_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "export-data"
ESI_SCHEMA_PATH = (
    Path.home() / "projects" / "tmp" / "eve-argus-quick" / "esi-schema" / "openapi.json"
)
ESI_URL = "https://esi.evetech.net/latest"

cache = EsiMemoryCache()
eve_openapi = EveOpenApi(spec_path=ESI_SCHEMA_PATH)
esi_client = ArgusAiohttpClient(
    cache=cache,
    api_spec=eve_openapi,
    base_url=ESI_URL,
    user_agent_prefix="Eve Argus Script Testing",
)

static_reader = ArgusFileReader(ARGUS_STATIC_DATA)
static_writer = ArgusFileWriter(ARGUS_STATIC_DATA)
esi_reader = ArgusFileReader(ARGUS_STATIC_DATA)
esi_writer = ArgusFileWriter(ARGUS_ESI_DATA)


def fetch_market_history(region_id: int, type_ids: list[int]) -> None:
    start = perf_counter()
    print(f"Requesting the market history for {len(type_ids)} type IDs in {region_id}")
    regional_history = FETCH.regional_market_history(
        esi_client=esi_client,
        region_id=region_id,
        type_ids=type_ids,
    )
    print(
        f"Received market history for {len(regional_history.data)} type IDs in {perf_counter() - start:.2f} seconds"
    )
    write_start = perf_counter()
    esi_writer.regional_market_history(regional_history)
    print(
        f"Wrote market history to {ARGUS_ESI_DATA} in {perf_counter() - write_start:.2f} seconds"
    )


def industry_type_ids(type_id_subset: TypeIDSubsets) -> list[int]:
    all_industry = type_id_subset.industry_related.type_ids
    blueprints = type_id_subset.blueprints.type_ids
    indy_market = all_industry - blueprints
    return list(indy_market)


def fetch_market_types(region_id: int) -> EAM.RegionalMarketTypes:
    start = perf_counter()
    print(f"Requesting market types for region {region_id}")
    regional_types = FETCH.market_types(esi_client=esi_client, region_id=region_id)
    print(
        f"Received market types for region {region_id} in {perf_counter() - start:.2f} seconds"
    )
    return regional_types


def main() -> None:
    start = perf_counter()
    region_id = 10000002  # Example region ID for The Forge
    type_id_subset = esi_reader.type_id_subsets()
    print(f"Loaded type ID subsets in {perf_counter() - start:.2f} seconds")

    indy_market = industry_type_ids(type_id_subset)
    print(f"Found {len(indy_market)} industry-related type IDs")
    market_types = fetch_market_types(region_id)
    print(f"Found {len(market_types.type_ids)} market types for region {region_id}")
    market_union = set(indy_market) & market_types.type_ids
    print(f"Total market types to fetch: {len(market_union)}")
    # test_list = [34, 35]
    # fetch_market_history(region_id, test_list)
    fetch_market_history(region_id, list(market_union))


if __name__ == "__main__":
    main()
