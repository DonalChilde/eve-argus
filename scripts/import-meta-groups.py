# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///


from pathlib import Path
from time import perf_counter

from eve_argus.file_loader import ArgusLoader, ArgusWriter, SdeLoader
from eve_argus.util.sde import import_meta_groups

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    print("Hello from import-meta-groups.py!")
    sde_reader = SdeLoader(sde_path=SDE_ROOT)
    argus_reader = ArgusLoader(argus_path=EVE_ARGUS_DATA)
    argus_writer = ArgusWriter(argus_path=EVE_ARGUS_DATA)
    sde_meta_groups = sde_reader.load_meta_groups()
    argus_meta_groups = import_meta_groups(sde_meta_groups=sde_meta_groups)
    argus_writer.meta_groups_to_json(meta_groups=argus_meta_groups)


if __name__ == "__main__":
    main()
