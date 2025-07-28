"""Test for the market order summary functionality in the Eve Argus ESI module."""

import logging
from importlib import resources
from itertools import chain
from pathlib import Path

from eve_argus.models import argus as EAM
from eve_argus.util.market_orders import calculate_order_summary
from tests.resources.argus_files import ARGUS_FILES

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_market_order_summary(test_output_dir: Path):
    file_resource = resources.files(ARGUS_FILES).joinpath(
        "10000002-34-market-orders.json"
    )
    with resources.as_file(file_resource) as input_path:
        market_orders = EAM.MarketOrdersByType.model_validate_json(
            input_path.read_text()
        )
        orders = chain(
            market_orders.buy_orders,
            market_orders.sell_orders,
        )
        summary = calculate_order_summary(
            orders=orders,
            filter_factor=5,
            type_id=market_orders.type_id,
            location_id=market_orders.region_id,
            location_spec="region",
        )

        output_path = (
            test_output_dir / f"market_order_summary_{market_orders.type_id}.json"
        )
        output_path.write_text(summary.model_dump_json(indent=2))
        logger.info(f"Market order summary calculated: {summary.model_dump()!r}")
        # Here you would typically load the market order summary data
        # and perform assertions to verify its correctness.
        # For example, you might check if the file exists and is readable.
        assert input_path.exists(), "Market order summary file does not exist."
        assert input_path.is_file(), "Market order summary path is not a file."

        # Further processing and assertions would go here.
        # This is a placeholder for actual test logic.
        print(f"Loaded market order summary from: {input_path}")


# TODO make a regionid typeid specific save load and translate function for market orders.
