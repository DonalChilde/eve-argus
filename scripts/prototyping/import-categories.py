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
from eve_argus.util.sde import import_categories

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    print("Hello from import-categories.py!")
    sde_reader = SdeLoader(sde_path=SDE_ROOT)
    argus_reader = ArgusFileReader(argus_path=EVE_ARGUS_DATA)
    argus_writer = ArgusFileWriter(argus_path=EVE_ARGUS_DATA)
    sde_categories = sde_reader.load_categories()
    argus_categories = import_categories(sde_categories=sde_categories)
    argus_writer.categories_to_json(categories=argus_categories)


if __name__ == "__main__":
    main()
