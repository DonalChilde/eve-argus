"""Module for the Eve Argus class."""

import logging
from pathlib import Path
from time import perf_counter
from typing import Any, Sequence

from eve_argus import CONFIG
from eve_argus.data_import.esi_requests import EsiPublic
from eve_argus.data_import.sde_to_argus import import_data_from_sde
from eve_argus.file_io.argus_data_file_reader import ArgusFileReader
from eve_argus.file_io.argus_data_file_writer import ArgusFileWriter

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class EveArgus:
    """Main class for Eve Argus operations."""

    def __init__(
        self,
        user_agent: str = "Eve Argus Client",
        sde_path: Path | None = None,
        argus_path: Path | None = None,
        debug: bool = False,
        debug_path: Path | None = None,
    ):
        """Initialize the Eve Argus client."""
        self.user_agent = user_agent
        self.debug = debug
        self.debug_path = debug_path or CONFIG["debug_path"]
        self.sde_path = sde_path or CONFIG["default_sde_path"]
        self.argus_path = argus_path or CONFIG["default_app_data_path"]
        self.writer = ArgusFileWriter(argus_path=self.argus_path)
        self.reader = ArgusFileReader(argus_path=self.argus_path)
        self.esi_public = EsiPublic(
            user_agent=user_agent, debug=debug, debug_path=debug_path
        )
        logger.info("Eve Argus client initialized.")

    def update_static_data(self) -> None:
        """Update static data from SDE to Argus."""
        start = perf_counter()
        logger.info("Updating static data from SDE to Argus.")
        import_data_from_sde(
            sde_path=self.sde_path,
            argus_path=self.argus_path,
            lang="en",
            effective_date=None,
            sde_version=None,
        )
        logger.info(
            f"Static data update complete in {perf_counter() - start:.6f} seconds."
        )

    def update_general_market_data(self) -> None:
        """Update general market data from ESI."""
        start = perf_counter()
        logger.info("Updating general market data from ESI.")

        universe_market_prices = self.esi_public.get_universe_market_prices()
        self.writer.universe_market_prices(universe_market_prices, overwrite=True)

        system_cost_indices = self.esi_public.get_system_cost_indices()
        self.writer.system_cost_indices(system_cost_indices, overwrite=True)

        logger.info(
            f"General market data update complete in {perf_counter() - start:.6f} seconds."
        )

    def update_market_orders(self, region_id: int) -> None:
        """Update market orders for a specific region."""
        start = perf_counter()
        logger.info(f"Updating market orders for region {region_id}.")

        market_orders = self.esi_public.get_market_orders_by_region(region_id=region_id)
        self.writer.regional_market_orders(
            regional_market_orders=market_orders, overwrite=True
        )

        logger.info(
            f"Market orders updated for region {region_id} complete in {perf_counter() - start:.6f} seconds."
        )

    def type_id_to_name(self, type_id: int) -> str:
        """Convert a type ID to its name."""
        # This method would typically query the ESI or a local database
        # to get the name of the type based on its ID.
        # Placeholder implementation for demonstration purposes.
        # FIXME: Replace with actual implementation.
        return f"Type Name for ID {type_id}"

    def update_eiv(self) -> None:
        """Update EIV data."""
        start = perf_counter()
        logger.info("Updating EIV data.")

        # FIXME: Placeholder for EIV update logic

    def update_unit_cost(
        self,
        material_prices: dict[int, int],
        structure: Any,
        character: Any,
        type_ids: Sequence[int],
    ) -> None:
        """Update unit cost data."""
        start = perf_counter()
        logger.info("Updating unit cost data.")

        # FIXME: Placeholder for unit cost update logic
        # this stub is more of a reminder to implement the actual logic
        # at the top level, the params are likely to be different.
