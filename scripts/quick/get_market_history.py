# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

from pathlib import Path
from time import perf_counter

from eve_argus.argus_esi.argus_esi import regional_market_history
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


def main() -> None:
    start = perf_counter()
    region_id = 10000002  # Example region ID for The Forge
    type_id_subset = esi_reader.type_id_subsets()
    print(f"Loaded type ID subsets in {perf_counter() - start:.2f} seconds")
    all_industry = type_id_subset.industry_related.type_ids
    blueprints = type_id_subset.blueprints.type_ids
    indy_market = all_industry - blueprints
    print(
        f"Requesting the market history for {len(indy_market)} type IDs in {region_id}"
    )
    request_start = perf_counter()
    regional_history = regional_market_history(
        esi_client=esi_client,
        region_id=region_id,
        type_ids=list(indy_market),
    )
    print(
        f"Received market history for {len(regional_history.data)} type IDs in {perf_counter() - request_start:.2f} seconds"
    )
    write_start = perf_counter()
    esi_writer.regional_market_history(regional_history)
    print(
        f"Wrote market history to {ARGUS_ESI_DATA} in {perf_counter() - write_start:.2f} seconds"
    )


if __name__ == "__main__":
    main()
