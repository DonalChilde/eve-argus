# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///


from time import perf_counter
from pathlib import Path
from eve_argus.file_loader import SdeLoader, ArgusLoader, ArgusWriter
from eve_argus.util.sde import import_groups

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    print("Hello from import-groups.py!")
    sde_reader = SdeLoader(sde_path=SDE_ROOT)
    argus_reader = ArgusLoader(argus_path=EVE_ARGUS_DATA)
    argus_writer = ArgusWriter(argus_path=EVE_ARGUS_DATA)
    sde_groups = sde_reader.load_groups()
    argus_groups = import_groups(sde_groups=sde_groups)
    argus_writer.groups_to_json(groups=argus_groups)


if __name__ == "__main__":
    main()
