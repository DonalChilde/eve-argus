# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from pathlib import Path
from time import perf_counter

from eve_argus.esi import EsiPublic
from eve_argus.file_loader import ArgusWriter

save_path = Path.home() / "projects" / "tmp" / "eve-argus" / "sample-data"


def get_market_history(esi: EsiPublic, region_id: int, type_id: int):
    start = perf_counter()
    data = esi.get_market_history(region_id=region_id, type_id=type_id)
    writer = ArgusWriter(argus_path=save_path)
    writer.market_history_to_json(
        region_id=region_id, type_id=type_id, market_history=data, overwrite=True
    )
    print(
        f"Wrote market history for ({region_id}, {type_id}) to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def get_market_prices_universe(esi: EsiPublic):
    start = perf_counter()
    data = esi.get_market_prices_universe()
    writer = ArgusWriter(argus_path=save_path)
    writer.market_prices_universe_to_json(data, overwrite=True)
    print(
        f"Wrote market prices to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def get_region_market_types(esi: EsiPublic, region_id: int):
    start = perf_counter()
    data = esi.get_region_market_types(region_id=region_id)
    writer = ArgusWriter(argus_path=save_path)
    writer.region_market_types_to_json(data, region_id=region_id, overwrite=True)
    print(
        f"Wrote region market types for {region_id} to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def get_market_orders(esi: EsiPublic, region_id: int):
    start = perf_counter()
    data = esi.get_market_orders(region_id=region_id)
    writer = ArgusWriter(argus_path=save_path)
    writer.market_orders_to_json(data, overwrite=True)
    print(
        f"Wrote market orders for {region_id} to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def main() -> None:
    print("Hello from sample-data.py!")
    esi = EsiPublic(debug=True, debug_path=save_path)

    region_id = 10000002  # The Forge region ID
    type_id = 34
    get_market_history(esi, region_id, type_id)
    get_market_prices_universe(esi)
    get_region_market_types(esi, region_id)
    get_market_orders(esi, region_id)


if __name__ == "__main__":
    main()
