# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///


from time import perf_counter
from pathlib import Path
from eve_argus.file_loader import SdeLoader, ArgusLoader, ArgusWriter
from eve_argus.util.sde import import_categories

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    print("Hello from import-categories.py!")
    sde_reader = SdeLoader(sde_path=SDE_ROOT)
    argus_reader = ArgusLoader(argus_path=EVE_ARGUS_DATA)
    argus_writer = ArgusWriter(argus_path=EVE_ARGUS_DATA)
    sde_categories = sde_reader.load_categories()
    argus_categories = import_categories(sde_categories=sde_categories)
    argus_writer.categories_to_json(categories=argus_categories)


if __name__ == "__main__":
    main()
