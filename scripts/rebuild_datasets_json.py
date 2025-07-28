# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

from pathlib import Path
from time import perf_counter

from eve_argus.data_import.argus_data_file_loader import (
    ArgusFileReader,
    ArgusFileWriter,
    SdeLoader,
)
from eve_argus.esi import EsiPublic
from eve_argus.util import argus as ARGUS_UTIL
from eve_argus.util import sde as SDE_UTIL

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"

sde_loader = SdeLoader(sde_path=SDE_ROOT)
argus_loader = ArgusFileReader(argus_path=EVE_ARGUS_DATA)
argus_writer = ArgusFileWriter(argus_path=EVE_ARGUS_DATA)


def localize_sde_types():
    """Localize SDE types and split out descriptions."""
    start = perf_counter()
    print("\nLocalizing SDE types, and splitting out descriptions.")
    print(f"Loading SDE type data.")
    sde_types = sde_loader.load_types()
    print(f"Data loaded in {perf_counter() - start:.6f} seconds")
    print(f"Found {len(sde_types)} type entries in SDE.")

    conversion_start = perf_counter()
    types, descriptions = SDE_UTIL.import_sde_types(sde_types=sde_types)
    print(f"Imported {len(types)} types.")
    print(f"Imported {len(descriptions)} type descriptions.")
    print(
        f"Conversion to Argus models completed in {perf_counter() - conversion_start:.6f} seconds."
    )

    convert_csv = perf_counter()
    path_out = argus_writer.type_info_to_csv(type_info=types)
    print(f"Type info written to CSV at {path_out}.")
    path_out = argus_writer.type_description_to_csv(type_description=descriptions)
    print(f"Type description written to CSV at {path_out}.")
    print(f"Data written to CSV in {perf_counter() - convert_csv:.6f} seconds.")

    convert_json = perf_counter()
    path_out = argus_writer.type_info_to_json(type_info=types)
    print(f"Type info written to JSON at {path_out}.")
    path_out = argus_writer.type_description_to_json(type_description=descriptions)
    print(f"Type description written to JSON at {path_out}.")
    print(f"Data written to JSON in {perf_counter() - convert_json:.6f} seconds.")


def import_blueprints():
    """Import blueprints from SDE."""
    start = perf_counter()
    print("\nImporting blueprints from SDE.")
    blueprints = sde_loader.load_blueprints()
    print(
        f"Loaded {len(blueprints)} blueprints in {perf_counter() - start:.6f} seconds."
    )

    conversion_start = perf_counter()
    print("Converting SDE blueprints to Argus models.")
    argus_blueprints = SDE_UTIL.import_blueprints(sde_blueprints=blueprints)
    print(
        f"Converted {len(argus_blueprints)} blueprints in {perf_counter() - conversion_start:.6f} seconds."
    )

    write_start = perf_counter()
    print("Writing blueprints to JSON.")
    path_out = argus_writer.blueprints_to_json(blueprints=argus_blueprints)
    print(f"Blueprints written to {path_out}.")
    print(
        f"Wrote {len(argus_blueprints)} blueprints to JSON in {perf_counter() - write_start:.6f} seconds."
    )


def import_categories():
    """Import categories from SDE."""
    start = perf_counter()
    print("\nImporting categories from SDE.")
    sde_categories = sde_loader.load_categories()
    print(
        f"Loaded {len(sde_categories)} categories in {perf_counter() - start:.6f} seconds."
    )

    conversion_start = perf_counter()
    print("Converting SDE categories to Argus models.")
    argus_categories = SDE_UTIL.import_categories(sde_categories=sde_categories)
    print(
        f"Converted {len(argus_categories)} categories in {perf_counter() - conversion_start:.6f} seconds."
    )

    write_start = perf_counter()
    print("Writing categories to JSON.")
    path_out = argus_writer.categories_to_json(categories=argus_categories)
    print(f"Categories written to {path_out}.")
    print(
        f"Wrote {len(argus_categories)} categories to JSON in {perf_counter() - write_start:.6f} seconds."
    )


def import_groups():
    """Import groups from SDE."""
    start = perf_counter()
    print("\nImporting groups from SDE.")
    sde_groups = sde_loader.load_groups()
    print(f"Loaded {len(sde_groups)} groups in {perf_counter() - start:.6f} seconds.")

    conversion_start = perf_counter()
    print("Converting SDE groups to Argus models.")
    argus_groups = SDE_UTIL.import_groups(sde_groups=sde_groups)
    print(
        f"Converted {len(argus_groups)} groups in {perf_counter() - conversion_start:.6f} seconds."
    )

    write_start = perf_counter()
    print("Writing groups to JSON.")
    path_out = argus_writer.groups_to_json(groups=argus_groups)
    print(f"Groups written to {path_out}.")
    print(
        f"Wrote {len(argus_groups)} groups to JSON in {perf_counter() - write_start:.6f} seconds."
    )


def import_market_groups():
    """Import market groups from SDE."""
    start = perf_counter()
    print("\nImporting market groups from SDE.")
    sde_market_groups = sde_loader.load_market_groups()
    print(
        f"Loaded {len(sde_market_groups)} market groups in {perf_counter() - start:.6f} seconds."
    )

    conversion_start = perf_counter()
    print("Converting SDE market groups to Argus models.")
    argus_market_groups = SDE_UTIL.import_market_groups(
        sde_market_groups=sde_market_groups
    )
    print(
        f"Converted {len(argus_market_groups)} market groups in {perf_counter() - conversion_start:.6f} seconds."
    )

    write_start = perf_counter()
    print("Writing market groups to JSON.")
    path_out = argus_writer.market_groups_to_json(market_groups=argus_market_groups)
    print(f"Market groups written to {path_out}.")
    print(
        f"Wrote {len(argus_market_groups)} market groups to JSON in {perf_counter() - write_start:.6f} seconds."
    )


def import_meta_groups():
    """Import meta groups from SDE."""
    start = perf_counter()
    print("\nImporting meta groups from SDE.")
    sde_meta_groups = sde_loader.load_meta_groups()
    print(
        f"Loaded {len(sde_meta_groups)} meta groups in {perf_counter() - start:.6f} seconds."
    )

    conversion_start = perf_counter()
    print("Converting SDE meta groups to Argus models.")
    argus_meta_groups = SDE_UTIL.import_meta_groups(sde_meta_groups=sde_meta_groups)
    print(
        f"Converted {len(argus_meta_groups)} meta groups in {perf_counter() - conversion_start:.6f} seconds."
    )

    write_start = perf_counter()
    print("Writing meta groups to JSON.")
    path_out = argus_writer.meta_groups_to_json(meta_groups=argus_meta_groups)
    print(f"Meta groups written to {path_out}.")
    print(
        f"Wrote {len(argus_meta_groups)} meta groups to JSON in {perf_counter() - write_start:.6f} seconds."
    )


def get_published_type_ids():
    """Get type IDs that are published."""
    start = perf_counter()
    print("\nGetting published type IDs from Argus data.")
    type_dict = argus_loader.type_info()
    print(
        f"Loaded {len(type_dict.data)} type entries in {perf_counter() - start:.6f} seconds."
    )

    conversion_start = perf_counter()
    print("Filtering published type IDs.")
    published_type_ids = ARGUS_UTIL.published_type_ids(type_dict=type_dict)
    print(
        f"Found {len(published_type_ids.type_ids)} published type IDs in {perf_counter() - conversion_start:.6f} seconds."
    )

    save_start = perf_counter()
    print("Saving published type IDs to JSON.")
    path_out = argus_writer.type_ids_published_to_json(type_ids=published_type_ids)
    print(
        f"Published type IDs saved to {path_out} in {perf_counter() - save_start:.6f} seconds."
    )


def get_type_ids_used_in_blueprints():
    """Get published type IDs used in blueprints."""
    start = perf_counter()
    print("\nGetting type IDs used in blueprints from Argus data.")
    blueprints = argus_loader.blueprints()
    print(
        f"Loaded {len(blueprints.data)} blueprints in {perf_counter() - start:.6f} seconds."
    )

    print("Getting published type IDs for filtering.")
    published_type_ids = argus_loader.type_ids_published()
    print(
        f"Loaded {len(published_type_ids.type_ids)} published type IDs in {perf_counter() - start:.6f} seconds."
    )

    conversion_start = perf_counter()
    print("Filtering for published type IDs used in blueprints.")
    type_ids_used = ARGUS_UTIL.get_type_ids_used_in_blueprints(blueprints=blueprints)
    print(
        f"Found {len(type_ids_used.type_ids)} type IDs used in blueprints in {perf_counter() - conversion_start:.6f} seconds."
    )

    save_start = perf_counter()
    print("Saving type IDs used in blueprints to JSON.")
    path_out = argus_writer.type_ids_in_blueprints_to_json(type_ids=type_ids_used)
    print(
        f"Type IDs used in blueprints saved to {path_out} in {perf_counter() - save_start:.6f} seconds."
    )


def get_published_type_ids_possible_in_market():
    """Get type IDs that are possible in the market."""
    start = perf_counter()
    print("\nGetting type IDs possible in the market from Argus data.")
    eve_types = argus_loader.type_info()
    print(
        f"Loaded {len(eve_types.data)} type entries in {perf_counter() - start:.6f} seconds."
    )

    conversion_start = perf_counter()
    print("Filtering for type IDs possible in the market.")
    type_ids_possible = ARGUS_UTIL.get_type_ids_possible_in_market(
        eve_types=eve_types, filter_published=True
    )
    print(
        f"Found {len(type_ids_possible.type_ids)} type IDs possible in the market in {perf_counter() - conversion_start:.6f} seconds."
    )

    save_start = perf_counter()
    print("Saving type IDs possible in the market to JSON.")
    path_out = argus_writer.type_ids_in_market_to_json(type_ids=type_ids_possible)
    print(
        f"Type IDs possible in the market saved to {path_out} in {perf_counter() - save_start:.6f} seconds."
    )


def get_type_ids_needed_for_industry_pricing():
    """Get type IDs needed for industry pricing."""
    start = perf_counter()
    print("\nGetting type IDs needed for industry pricing from Argus data.")
    market_type_ids = argus_loader.type_ids_in_market()
    blueprint_type_ids = argus_loader.type_ids_in_blueprints()
    print(
        f"Loaded {len(market_type_ids.type_ids)} market type IDs and {len(blueprint_type_ids.type_ids)} blueprint type IDs in {perf_counter() - start:.6f} seconds."
    )

    conversion_start = perf_counter()
    print("Filtering for type IDs needed for industry pricing.")
    type_ids_needed = ARGUS_UTIL.get_type_ids_needed_for_industry_pricing(
        market_type_ids=market_type_ids, blueprint_type_ids=blueprint_type_ids
    )
    print(
        f"Found {len(type_ids_needed.type_ids)} type IDs needed for industry pricing in {perf_counter() - conversion_start:.6f} seconds."
    )

    save_start = perf_counter()
    print("Saving type IDs needed for industry pricing to JSON.")
    path_out = argus_writer.type_ids_for_industry_pricing_to_json(
        type_ids=type_ids_needed
    )
    print(
        f"Type IDs needed for industry pricing saved to {path_out} in {perf_counter() - save_start:.6f} seconds."
    )


def main() -> None:
    start = perf_counter()
    print("Rebuilding datasets from SDE data")
    localize_sde_types()
    import_blueprints()
    import_groups()
    import_categories()
    import_market_groups()
    import_meta_groups()
    get_published_type_ids()
    get_type_ids_used_in_blueprints()
    get_published_type_ids_possible_in_market()
    get_type_ids_needed_for_industry_pricing()
    print(f"All datasets rebuilt successfully in {perf_counter() - start:.6f} seconds.")


if __name__ == "__main__":
    main()
