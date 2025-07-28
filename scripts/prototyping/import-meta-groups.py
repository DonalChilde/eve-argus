# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///


from pathlib import Path
from time import perf_counter

from eve_argus.calculations.sde import import_meta_groups
from eve_argus.data_import.argus_data_file_reader import (
    ArgusFileReader,
    ArgusFileWriter,
    SdeLoader,
)

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    print("Hello from import-meta-groups.py!")
    sde_reader = SdeLoader(sde_path=SDE_ROOT)
    argus_reader = ArgusFileReader(argus_path=EVE_ARGUS_DATA)
    argus_writer = ArgusFileWriter(argus_path=EVE_ARGUS_DATA)
    sde_meta_groups = sde_reader.load_meta_groups()
    argus_meta_groups = import_meta_groups(sde_meta_groups=sde_meta_groups)
    argus_writer.meta_groups_to_json(meta_groups=argus_meta_groups)


if __name__ == "__main__":
    main()
