# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///


from pathlib import Path
from time import perf_counter

from eve_argus.calculations.sde import import_groups
from eve_argus.file_io.argus_data_file_reader import (
    ArgusFileReader,
    ArgusFileWriter,
    SdeLoader,
)

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    print("Hello from import-groups.py!")
    sde_reader = SdeLoader(sde_path=SDE_ROOT)
    argus_reader = ArgusFileReader(argus_path=EVE_ARGUS_DATA)
    argus_writer = ArgusFileWriter(argus_path=EVE_ARGUS_DATA)
    sde_groups = sde_reader.load_groups()
    argus_groups = import_groups(sde_groups=sde_groups)
    argus_writer.groups_to_json(groups=argus_groups)


if __name__ == "__main__":
    main()
