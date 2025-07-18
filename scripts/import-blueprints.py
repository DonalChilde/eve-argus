# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from pathlib import Path
from time import perf_counter

from eve_argus.file_loader import ArgusLoader, ArgusWriter, SdeLoader
from eve_argus.util.argus import get_type_ids_used_in_blueprints, published_type_ids
from eve_argus.util.sde import import_blueprints

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    print("Hello from test_blueprint.py!")
    sde_reader = SdeLoader(sde_path=SDE_ROOT)
    argus_reader = ArgusLoader(argus_path=EVE_ARGUS_DATA)
    argus_writer = ArgusWriter(argus_path=EVE_ARGUS_DATA)
    type_info = argus_reader.type_info()
    print(
        f"Loaded {len(type_info.data)} type info in {perf_counter() - start:.6f} seconds."
    )
    sde_start = perf_counter()
    sde_blueprints = sde_reader.load_blueprints()
    print(f"Loaded sde blueprints in {perf_counter() - sde_start:.6f} seconds.")
    conversion_start = perf_counter()
    blueprints = import_blueprints(sde_blueprints=sde_blueprints)
    print(
        f"imported {len(blueprints)} sde blueprints in {perf_counter() - conversion_start:.6f} seconds."
    )
    bp_write_start = perf_counter()
    argus_writer.blueprints_to_json(blueprints=blueprints)
    print(
        f"Saved {len(blueprints)} Argus blueprints in {perf_counter() - bp_write_start:.6f} seconds."
    )
    load_bp_start = perf_counter()
    loaded_bp = argus_reader.blueprints()
    print(
        f"Loaded {len(loaded_bp.data)} Argus blueprints in {perf_counter() - load_bp_start:.6f} seconds."
    )
    unpublished_bp = 0
    published_ids = published_type_ids(type_dict=type_info)
    print(f"Found {len(published_ids)} in type info.")
    for key in loaded_bp.data.keys():
        if key not in published_ids:
            unpublished_bp += 1
    print(f"Found {unpublished_bp} unpublished blueprints.")
    used_type_ids = get_type_ids_used_in_blueprints(loaded_bp)
    unpublished_types = 0
    for type_id in used_type_ids:
        if type_id not in published_ids:
            unpublished_types += 1
    print(
        f"Found {len(used_type_ids)} type_ids in blueprints, {unpublished_types} are unpublished."
    )


if __name__ == "__main__":
    main()
