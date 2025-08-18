# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

from pathlib import Path
from time import perf_counter

from eve_argus.argus_esi.argus_esi import market_orders
from eve_argus.eve_argus_esi.esi_cache.esi_memory_cache import EsiMemoryCache
from eve_argus.eve_argus_esi.esi_client.aiohttp_client import (
    ArgusAiohttpClient,
)
from eve_argus.eve_argus_esi.esi_schema.eve_openapi import EveOpenApi
from eve_argus.file_io.argus_data_file_reader import ArgusFileReader
from eve_argus.file_io.argus_data_file_writer import ArgusFileWriter

ARGUS_STATIC_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "static-data"
ARGUS_ESI_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "esi-data"
ARGUS_EXPORT_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "export-data"
ESI_SCHEMA_PATH = (
    Path.home() / "projects" / "tmp" / "eve-argus-quick" / "esi-schema" / "openapi.json"
)
ESI_URL = "https://esi.evetech.net/latest"

static_reader = ArgusFileReader(ARGUS_STATIC_DATA)
static_writer = ArgusFileWriter(ARGUS_STATIC_DATA)
esi_reader = ArgusFileReader(ARGUS_ESI_DATA)
esi_writer = ArgusFileWriter(ARGUS_ESI_DATA)

cache = EsiMemoryCache()
eve_openapi = EveOpenApi(spec_path=ESI_SCHEMA_PATH)
esi_client = ArgusAiohttpClient(
    cache=cache,
    api_spec=eve_openapi,
    base_url=ESI_URL,
    user_agent_prefix="Eve Argus Script Testing",
)


def get_region_orders(region_id: int) -> None:
    start = perf_counter()
    orders = market_orders(esi_client=esi_client, region_id=region_id)
    print(
        f"Fetched market orders for region ID {region_id} in {perf_counter() - start:.2f} seconds"
    )
    write_start = perf_counter()
    esi_writer.regional_market_orders(orders)
    print(
        f"Wrote market orders for region ID {region_id} in {perf_counter() - write_start:.2f} seconds"
    )


def main() -> None:
    region_id = 10000002  # Example region ID for The Forge
    start = perf_counter()
    print(f"Fetching market orders for region ID: {region_id}")
    print(f"\tArgus ESI Data Path: {ARGUS_ESI_DATA}")

    get_region_orders(region_id)
    print(f"Total time taken: {perf_counter() - start:.2f} seconds")


if __name__ == "__main__":
    main()
