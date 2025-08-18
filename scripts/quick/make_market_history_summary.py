# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from pathlib import Path

from eve_argus.data_transform.summarize_market_history import (
    summarize_regional_market_history,
)
from eve_argus.file_io.argus_data_file_reader import ArgusFileReader
from eve_argus.file_io.argus_data_file_writer import ArgusFileWriter

ARGUS_STATIC_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "static-data"
ARGUS_ESI_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "esi-data"
ARGUS_EXPORT_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "export-data"

static_reader = ArgusFileReader(ARGUS_STATIC_DATA)
static_writer = ArgusFileWriter(ARGUS_STATIC_DATA)
esi_reader = ArgusFileReader(ARGUS_ESI_DATA)
esi_writer = ArgusFileWriter(ARGUS_ESI_DATA)


def generate_summary(region_id: int):
    """Generate a market history summary for a specific region."""
    print(f"Generating market history summary for region {region_id}")
    market_history = esi_reader.regional_market_history(region_id=region_id)
    history_summaries = summarize_regional_market_history(market_history, periods=[10])
    esi_writer.market_history_summaries(history_summaries)


def main() -> None:
    region_id = 10000002
    generate_summary(region_id)


if __name__ == "__main__":
    main()
