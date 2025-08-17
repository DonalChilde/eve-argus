# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

from pathlib import Path
from time import perf_counter

from eve_argus.argus_sde.argus_sde import import_data_from_sde
from eve_argus.file_io.argus_data_file_reader import ArgusFileReader
from eve_argus.file_io.argus_data_file_writer import ArgusFileWriter

SDE_PATH = Path.home() / "projects" / "eve-sde"
ARGUS_STATIC_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "static-data"
ARGUS_ESI_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "esi-data"
ARGUS_EXPORT_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "export-data"

static_reader = ArgusFileReader(ARGUS_STATIC_DATA)
static_writer = ArgusFileWriter(ARGUS_STATIC_DATA)
esi_reader = ArgusFileReader(ARGUS_ESI_DATA)
esi_writer = ArgusFileWriter(ARGUS_ESI_DATA)


def main() -> None:
    start = perf_counter()
    import_data_from_sde(sde_path=SDE_PATH, argus_path=ARGUS_STATIC_DATA)
    print(f"Import completed in {perf_counter() - start:.2f} seconds")


if __name__ == "__main__":
    print("Importing SDE data...")
    print(f"\tSDE Path: {SDE_PATH}")
    print(f"\tArgus Static Data Path: {ARGUS_STATIC_DATA}")
    main()
