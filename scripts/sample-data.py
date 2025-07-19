# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from pathlib import Path
from time import perf_counter

from eve_argus.esi import EsiPublic
from eve_argus.file_loader import ArgusWriter

save_path = Path.home() / "projects" / "tmp" / "eve-argus" / "sample-data"
argus_writer = ArgusWriter(argus_path=save_path)


def get_market_history(esi: EsiPublic, region_id: int, type_id: int):
    print(f"\nGetting market history for region {region_id}, type {type_id}.")
    start = perf_counter()
    data = esi.get_market_history(region_id=region_id, type_id=type_id)
    argus_writer.market_history_by_type_to_json(
        region_id=region_id, type_id=type_id, market_history=data, overwrite=True
    )
    print(
        f"Wrote market history for ({region_id}, {type_id}) to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def get_market_prices_universe(esi: EsiPublic):
    print("\nGetting market prices for the entire universe.")
    start = perf_counter()
    data = esi.get_market_prices_universe()
    argus_writer.market_prices_universe_to_json(data, overwrite=True)
    print(
        f"Wrote market prices to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def get_region_market_types(esi: EsiPublic, region_id: int):
    print(f"\nGetting market types for region {region_id}.")
    start = perf_counter()
    data = esi.get_region_market_types(region_id=region_id)
    argus_writer.region_market_types_to_json(data, region_id=region_id, overwrite=True)
    print(
        f"Wrote region market types for {region_id} to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def get_market_orders_by_region(esi: EsiPublic, region_id: int):
    print(f"\nGetting market orders for region {region_id}.")
    start = perf_counter()
    data = esi.get_market_orders_by_region(region_id=region_id)
    argus_writer.market_orders_by_region_to_json(
        market_orders_by_region=data, overwrite=True
    )
    print(
        f"Wrote market orders for {region_id} to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def get_market_orders_by_type(esi: EsiPublic, region_id: int, type_id: int):
    print(f"\nGetting market orders for region {region_id}, type {type_id}.")
    start = perf_counter()
    data = esi.get_market_orders_by_region_and_type(
        region_id=region_id, type_id=type_id
    )
    argus_writer.market_orders_by_region_and_type_to_json(
        market_orders_by_type=data, overwrite=True
    )
    print(
        f"Wrote market orders for ({region_id}, {type_id}) to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def main() -> None:
    start = perf_counter()
    print("Getting sample data from ESI...")
    debug_save_path = save_path / "debug"
    esi = EsiPublic(debug=True, debug_path=debug_save_path)
    print(f"Initialized EsiPublic client in {perf_counter() - start:.6f} seconds.")

    region_id = 10000002  # The Forge region ID
    type_id = 34  # Tritanium type ID
    get_market_history(esi, region_id, type_id)
    get_market_prices_universe(esi)
    get_region_market_types(esi, region_id)
    get_market_orders_by_type(esi, region_id, type_id)
    get_market_orders_by_region(esi, region_id)

    print(f"Total execution time: {perf_counter() - start:.6f} seconds.")


if __name__ == "__main__":
    main()
