# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

from pathlib import Path

from eve_argus.file_io.argus_data_file_reader import ArgusFileReader
from eve_argus.file_io.argus_data_file_writer import ArgusFileWriter

ARGUS_STATIC_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "static-data"
ARGUS_ESI_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "esi-data"
ARGUS_EXPORT_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "export-data"

static_reader = ArgusFileReader(ARGUS_STATIC_DATA)
static_writer = ArgusFileWriter(ARGUS_STATIC_DATA)
esi_reader = ArgusFileReader(ARGUS_ESI_DATA)
esi_writer = ArgusFileWriter(ARGUS_ESI_DATA)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
