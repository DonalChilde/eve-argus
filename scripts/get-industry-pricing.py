# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from collections.abc import Iterable, Sequence
from pathlib import Path
from time import perf_counter

from eve_argus.data_import.argus_data_file_loader import (
    ArgusFileReader,
    ArgusFileWriter,
)
from eve_argus.esi import EsiPublic
from eve_argus.models import argus as EAM
from eve_argus.util.market_history import summarize_regional_market_history
from eve_argus.util.market_orders import calculate_order_summaries

EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"
save_path = Path.home() / "projects" / "tmp" / "eve-argus" / "market-pricing"
argus_loader = ArgusFileReader(argus_path=EVE_ARGUS_DATA)
market_loader = ArgusFileReader(argus_path=save_path)
argus_writer = ArgusFileWriter(argus_path=save_path)

# 1. download region market orders
# 2. download market history for all industry type_ids in the region
# 3. calculate summaries for the market orders and write to file.
# 4. calculate summaries for the market history and write to file.
# 5. output market order summaries to csv files.
# 6. output market history summaries to csv files.


def get_market_orders_by_region(esi: EsiPublic, region_id: int) -> None:
    print(f"\nGetting market orders for region {region_id}.")
    start = perf_counter()
    data = esi.get_market_orders_by_region(region_id=region_id)
    argus_writer.market_orders_by_region_to_json(
        market_orders_by_region=data, overwrite=True
    )
    print(
        f"Wrote market orders for {region_id} to {save_path} in {perf_counter() - start:.6f} seconds."
    )


def get_market_history_by_region(
    esi: EsiPublic, region_id: int, type_ids: Sequence[int]
) -> None:
    print(
        f"\nGetting market history for region {region_id}, and {len(type_ids)} type IDs."
    )
    start = perf_counter()
    result = EAM.MarketHistoryByRegion(
        region_id=region_id,
        data={},
    )
    for type_id in type_ids:
        data = esi.get_market_history(region_id=region_id, type_id=type_id)
        result.data[type_id] = data
    print(
        f"Got {len(result.data)} type IDs of market history data in {perf_counter() - start:.6f} seconds."
    )
    write_start = perf_counter()
    argus_writer.market_history_by_region_to_json(market_history=result, overwrite=True)
    print(
        f"Wrote market history for {region_id} to {save_path} in {perf_counter() - write_start:.6f} seconds."
    )


def summarize_market_orders(
    orders: EAM.MarketOrdersByRegion, type_ids: Iterable[int] | None = None
) -> None:
    """Summarize market orders by type."""
    summaries = calculate_order_summaries(
        orders=orders,
        location_id=orders.region_id,
        location_spec="region",
        type_ids=type_ids,
    )
    write_start = perf_counter()
    argus_writer.market_order_summaries_by_region_to_json(
        region_id=orders.region_id,
        tag="industry",
        market_order_summaries=summaries,
        overwrite=True,
    )
    print(
        f"Wrote market order summaries for region {orders.region_id} to {save_path} in {perf_counter() - write_start:.6f} seconds."
    )


def summarize_market_history(
    history: EAM.MarketHistoryByRegion, type_ids: Iterable[int] | None = None
) -> None:
    """Summarize market history by type."""
    if type_ids is None:
        type_ids = history.data.keys()
    summaries = summarize_regional_market_history(
        history=history,
        type_ids=type_ids,
        periods=[10, 30, 60, 90],
    )
    write_start = perf_counter()
    argus_writer.market_history_summaries_by_region_to_json(
        tag="industry", market_history_summaries=summaries, overwrite=True
    )
    print(
        f"Wrote market history summaries for region {history.region_id} to {save_path} in {perf_counter() - write_start:.6f} seconds."
    )


def main() -> None:
    download = False
    print(f"Industry Market Pricing, {download=}")
    start = perf_counter()
    esi = EsiPublic(debug=True, debug_path=EVE_ARGUS_DATA / "debug")

    region_id = 10000002  # The Forge region ID
    print(f"Initialized EsiPublic client in {perf_counter() - start:.6f} seconds.")
    industry_ids = argus_loader.type_ids_for_industry_pricing()
    if download:
        # Wrote market orders for 10000002 to /home/chad/projects/tmp/eve-argus/market-pricing in 85.175930 seconds.
        # Got 6694 type IDs of market history data in 1181.908769 seconds.
        get_market_orders_by_region(esi, region_id=region_id)
        get_market_history_by_region(
            esi, region_id=region_id, type_ids=list(industry_ids.type_ids)
        )
    load_orders = perf_counter()
    orders = market_loader.market_orders_by_region(region_id=region_id)
    print(f"Loaded market orders in {load_orders - start:.6f} seconds.")
    summarize_market_orders(orders, type_ids=industry_ids.type_ids)
    load_history = perf_counter()
    history = market_loader.market_history_by_region(region_id=region_id)
    print(f"Loaded market history in {load_history - load_orders:.6f} seconds.")
    summarize_market_history(history=history, type_ids=industry_ids.type_ids)


if __name__ == "__main__":
    main()
