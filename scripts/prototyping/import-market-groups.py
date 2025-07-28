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
from eve_argus.util.sde import import_market_groups

SDE_ROOT = Path.home() / "projects" / "eve-sde"
EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    print("Hello from import-market-groups.py!")
    sde_reader = SdeLoader(sde_path=SDE_ROOT)
    argus_reader = ArgusFileReader(argus_path=EVE_ARGUS_DATA)
    argus_writer = ArgusFileWriter(argus_path=EVE_ARGUS_DATA)
    sde_market_groups = sde_reader.load_market_groups()
    argus_market_groups = import_market_groups(sde_market_groups=sde_market_groups)
    argus_writer.market_groups_to_json(market_groups=argus_market_groups)


if __name__ == "__main__":
    main()
