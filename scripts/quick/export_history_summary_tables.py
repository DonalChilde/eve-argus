# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

from pathlib import Path

from eve_argus.data_transform.market_history_summary_table import (
    market_history_summary_table,
)
from eve_argus.file_io.argus_data_file_reader import ArgusFileReader
from eve_argus.file_io.argus_data_file_writer import ArgusFileWriter
from eve_argus.snippets.file.csv import write_dicts_to_csv

ARGUS_STATIC_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "static-data"
ARGUS_ESI_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "esi-data"
ARGUS_EXPORT_DATA = Path.home() / "projects" / "tmp" / "eve-argus-quick" / "export-data"

static_reader = ArgusFileReader(ARGUS_STATIC_DATA)
static_writer = ArgusFileWriter(ARGUS_STATIC_DATA)
esi_reader = ArgusFileReader(ARGUS_ESI_DATA)
esi_writer = ArgusFileWriter(ARGUS_ESI_DATA)


def export_market_history_summary(region_id: int) -> None:
    market_history_summary = esi_reader.market_history_summaries(region_id)
    summary_table = market_history_summary_table(market_history_summary)
    file_path = ARGUS_EXPORT_DATA / f"market_history_summary_{region_id}.csv"
    write_dicts_to_csv(data=summary_table, file_path=file_path, overwrite=True)


def main() -> None:
    region_id = 10000002
    export_market_history_summary(region_id)


if __name__ == "__main__":
    main()
