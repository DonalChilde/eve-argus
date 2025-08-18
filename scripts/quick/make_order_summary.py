# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from pathlib import Path

from eve_argus.data_transform.summarize_market_orders import calculate_order_summaries
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
    """Generate a market order summary for a specific region."""
    print(f"Generating market order summary for region {region_id}")
    market_orders = esi_reader.regional_market_orders(region_id=region_id)
    order_summaries = calculate_order_summaries(
        market_orders, location_id=region_id, location_spec="region"
    )
    esi_writer.market_order_summaries(order_summaries, region_id=region_id)


def main() -> None:
    region_id = 10000002  # Example region ID, replace with actual
    generate_summary(region_id)


if __name__ == "__main__":
    main()
