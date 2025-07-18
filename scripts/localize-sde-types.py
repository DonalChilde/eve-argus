# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pyyaml",
# ]
# ///
from pathlib import Path
from time import perf_counter

from eve_argus.file_loader import ArgusWriter, SdeLoader
from eve_argus.util.sde import import_sde_types

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    print("Localizing sde types, and splitting out descriptions.")
    sde = SdeLoader(sde_path=SDE_ROOT)
    print(f"Loading sde type data.")
    sde_types = sde.load_types()
    print(f"Data loaded in {perf_counter() - start:.6f} seconds")
    print(f"Found {len(sde_types)} type entries in sde.")
    types, descriptions = import_sde_types(sde_types=sde_types)
    print(f"Imported {len(types)} types.")
    print(f"Imported {len(descriptions)} type descriptions.")
    convert_csv = perf_counter()
    writer = ArgusWriter(argus_path=EVE_ARGUS_DATA)
    writer.type_info_to_csv(type_info=types)
    writer.type_description_to_csv(type_description=descriptions)
    print(f"Types written to csv in {perf_counter() - convert_csv:.6f} seconds.")
    convert_json = perf_counter()
    writer.type_info_to_json(type_info=types)
    writer.type_description_to_json(type_description=descriptions)
    print(f"Data written to json in {perf_counter() - convert_json:.6f} seconds.")


if __name__ == "__main__":
    main()
