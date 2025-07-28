# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from collections.abc import Iterable
from pathlib import Path
from time import perf_counter

from eve_argus.data_import.argus_data_file_loader import (
    ArgusFileReader,
    ArgusFileWriter,
)
from eve_argus.snippets.file.csv import write_dicts_to_csv
from eve_argus.util import argus as ARGUS_UTIL

EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


argus_loader = ArgusFileReader(argus_path=EVE_ARGUS_DATA)
argus_writer = ArgusFileWriter(argus_path=EVE_ARGUS_DATA)


def build_info_table(file_name: str, type_ids: Iterable[int] | None = None) -> None:
    """Build the info table."""
    start_time = perf_counter()

    eve_types = argus_loader.type_info()
    print(
        f"Loaded {len(eve_types.data)} types in {perf_counter() - start_time:.2f} seconds."
    )

    print("Loading market groups...")
    market_groups = argus_loader.market_groups()
    print(
        f"Loaded {len(market_groups.data)} market groups in {perf_counter() - start_time:.2f} seconds."
    )
    meta_groups = argus_loader.meta_groups()
    categories = argus_loader.categories()
    groups = argus_loader.groups()
    print(
        f"Loaded {len(meta_groups.data)} meta groups, {len(categories.data)} categories, and {len(groups.data)} groups in {perf_counter() - start_time:.2f} seconds."
    )
    print("Building type info table...")
    type_info_table = ARGUS_UTIL.type_info_table(
        type_info=eve_types,
        type_ids=type_ids,
        market_groups=market_groups,
        meta_levels=meta_groups,
        groups=groups,
        categories=categories,
    )

    print("Writing type info table to file...")
    file_path = EVE_ARGUS_DATA / file_name
    write_dicts_to_csv(type_info_table, file_path, overwrite=True)
    print(f"Type info table written to {file_path}.")


def main() -> None:
    print("Hello from info_table.py!")
    build_info_table(type_ids=None, file_name="eve-type-info-all.csv")
    industry_type_ids = argus_loader.type_ids_for_industry_pricing()
    build_info_table(
        type_ids=industry_type_ids.type_ids, file_name="eve-type-info-industry.csv"
    )


if __name__ == "__main__":
    main()
