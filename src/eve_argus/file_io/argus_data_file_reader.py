"""File reader for the Argus data files."""

import logging
from pathlib import Path
from string import Template
from time import perf_counter

from eve_argus.file_io.argus_file_paths import ArgusFilePaths
from eve_argus.models import argus as EAM

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ArgusFileReader:
    def __init__(self, argus_path: Path) -> None:
        """API to load Argus specific data files."""
        self.argus_path = argus_path

    def system_cost_indices(self) -> EAM.SystemCostIndices:
        """Load system cost indices from JSON.

        Returns:
            EAM.SystemCostIndices: The system cost indices data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.SYSTEM_COST_INDICES
        result = EAM.SystemCostIndices.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def type_info(self) -> EAM.TypeInfos:
        """Load type information from JSON.

        Returns:
            EAM.TypeInfos: The type information data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.TYPE_INFO
        result = EAM.TypeInfos.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def type_description(self) -> EAM.TypeDescriptions:
        """Load type descriptions from JSON.

        Returns:
            EAM.TypeDescriptions: The type descriptions data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.TYPE_DESCRIPTION
        result = EAM.TypeDescriptions.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def blueprints(self) -> EAM.Blueprints:
        """Load blueprints from JSON.

        Returns:
            EAM.Blueprints: The blueprints data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.BLUEPRINTS
        result = EAM.Blueprints.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_groups(self) -> EAM.MarketGroups:
        """Load market groups from JSON.

        Returns:
            EAM.MarketGroups: The market groups data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.MARKET_GROUPS
        result = EAM.MarketGroups.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def meta_groups(self) -> EAM.MetaGroups:
        """Load meta groups from JSON.

        Returns:
            EAM.MetaGroups: The meta groups data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.META_GROUPS
        result = EAM.MetaGroups.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def groups(self) -> EAM.Groups:
        """Load groups from JSON.

        Returns:
            EAM.Groups: The groups data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.GROUPS
        result = EAM.Groups.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def categories(self) -> EAM.Categories:
        """Load categories from JSON.

        Returns:
            EAM.Categories: The categories data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.CATEGORIES
        result = EAM.Categories.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_prices_universe(self) -> EAM.UniverseMarketPrices:
        """Load market prices for the entire universe from JSON.

        Returns:
            EAM.UniverseMarketPrices: The universe market prices data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.MARKET_PRICES_UNIVERSE
        result = EAM.UniverseMarketPrices.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def type_id_subsets(self) -> EAM.TypeIDSubsets:
        """Get type ID subsets from Argus data.

        Returns:
            EAM.TypeIDSubsets: The type ID subsets data.
        """
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.TYPE_ID_SUBSETS
        result = EAM.TypeIDSubsets.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded type ID subsets in %s seconds",
            f"{perf_counter() - start:.6f}",
        )
        return result

    # def type_ids_published(self) -> EAM.TypeIDSubset:
    #     """Load published type IDs from JSON.

    #     Returns:
    #         EAM.TypeIDSubset: The published type IDs data.
    #     """
    #     start = perf_counter()
    #     path_in = self.argus_path / ArgusFilePaths.TYPE_IDS_PUBLISHED
    #     result = EAM.TypeIDSubset.model_validate_json(path_in.read_text())
    #     logger.info(
    #         "Loaded data from %s in %s seconds",
    #         path_in,
    #         f"{perf_counter() - start:.6f}",
    #     )
    #     return result

    # def type_ids_in_blueprints(self) -> EAM.TypeIDSubset:
    #     """Load type IDs that are used in blueprints from JSON.

    #     Returns:
    #         EAM.TypeIDSubset: The type IDs used in blueprints data.
    #     """
    #     start = perf_counter()
    #     path_in = self.argus_path / ArgusFilePaths.TYPE_IDS_IN_BLUEPRINTS
    #     result = EAM.TypeIDSubset.model_validate_json(path_in.read_text())
    #     logger.info(
    #         "Loaded data from %s in %s seconds",
    #         path_in,
    #         f"{perf_counter() - start:.6f}",
    #     )
    #     return result

    # def type_ids_in_market(self) -> EAM.TypeIDSubset:
    #     """Load type IDs that are possible in the market from JSON.

    #     Returns:
    #         EAM.TypeIDSubset: The type IDs possible in the market data.
    #     """
    #     start = perf_counter()
    #     path_in = self.argus_path / ArgusFilePaths.TYPE_IDS_IN_MARKET
    #     result = EAM.TypeIDSubset.model_validate_json(path_in.read_text())
    #     logger.info(
    #         "Loaded data from %s in %s seconds",
    #         path_in,
    #         f"{perf_counter() - start:.6f}",
    #     )
    #     return result

    # def type_ids_for_industry_pricing(self) -> EAM.TypeIDSubset:
    #     """Load type IDs that are needed for industry pricing from JSON.

    #     Returns:
    #         EAM.TypeIDSubset: The type IDs needed for industry pricing data.
    #     """
    #     start = perf_counter()
    #     path_in = self.argus_path / ArgusFilePaths.TYPE_IDS_FOR_INDUSTRY_PRICING
    #     result = EAM.TypeIDSubset.model_validate_json(path_in.read_text())
    #     logger.info(
    #         "Loaded data from %s in %s seconds",
    #         path_in,
    #         f"{perf_counter() - start:.6f}",
    #     )
    #     return result

    # def market_history(self, region_id: int, type_id: int) -> EAM.MarketHistory:
    #     """Load market history for a specific region and type from JSON.

    #     Args:
    #         region_id (int): The ID of the region.
    #         type_id (int): The ID of the type.

    #     Returns:
    #         EAM.MarketHistory: The market history data for the specified region and type.
    #     """
    #     start = perf_counter()
    #     path_in = (
    #         self.argus_path
    #         / ArgusFilePaths.ESI_DATA
    #         / Template(ArgusFilePaths.MARKET_HISTORY).substitute(
    #             region_id=region_id, type_id=type_id
    #         )
    #     )
    #     result = EAM.MarketHistory.model_validate_json(path_in.read_text())
    #     logger.info(
    #         "Loaded data from %s in %s seconds",
    #         path_in,
    #         f"{perf_counter() - start:.6f}",
    #     )
    #     return result

    # def market_histories(self, region_id: int) -> EAM.MarketHistories:
    #     """Load market history for a specific region from JSON.

    #     Args:
    #         region_id (int): The ID of the region.

    #     Returns:
    #         EAM.RegionalMarketHistory: The market history data for the specified region.
    #     """
    #     start = perf_counter()
    #     path_in = (
    #         self.argus_path
    #         / ArgusFilePaths.ESI_DATA
    #         / Template(ArgusFilePaths.MARKET_HISTORIES).substitute(region_id=region_id)
    #     )
    #     result = EAM.MarketHistories.model_validate_json(path_in.read_text())
    #     logger.info(
    #         "Loaded data from %s in %s seconds",
    #         path_in,
    #         f"{perf_counter() - start:.6f}",
    #     )
    #     return result

    def regional_market_orders(self, region_id: int) -> EAM.RegionalMarketOrders:
        """Load market orders for a specific region from JSON.

        Args:
            region_id (int): The ID of the region.

        Returns:
            EAM.RegionalMarketOrders: The market orders data for the specified region.
        """
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.REGIONAL_MARKET_ORDERS).substitute(
                region_id=region_id
            )
        )
        result = EAM.RegionalMarketOrders.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_orders(self, region_id: int, type_id: int) -> EAM.MarketOrders:
        """Load market orders for a specific region and type from JSON.

        Args:
            region_id (int): The ID of the region.
            type_id (int): The ID of the type.

        Returns:
            EAM.MarketOrders: The market orders data for the specified region and type.
        """
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDERS).substitute(
                region_id=region_id, type_id=type_id
            )
        )
        result = EAM.MarketOrders.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_history_summaries(
        self, region_id: int, tag: str = "all"
    ) -> EAM.MarketHistorySummaries:
        """Load market history summaries for a specific region from JSON.

        Args:
            region_id (int): The ID of the region.
            tag (str, optional): A tag to append to the filename. Defaults to "all".

        Returns:
            EAM.MarketHistorySummariesByRegion: The market history summaries for the specified region.
        """
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_HISTORY_SUMMARIES).substitute(
                region_id=region_id, tag=tag
            )
        )
        result = EAM.MarketHistorySummaries.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_order_summaries(
        self, region_id: int, tag: str = "all"
    ) -> EAM.MarketOrderSummaries:
        """Load market order summaries for a specific region from JSON.

        Args:
            region_id (int): The ID of the region.
            tag (str, optional): A tag to append to the filename. Defaults to "all".

        Returns:
            EAM.MarketOrderSummaries: The market order summaries for the specified region.
        """
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDER_SUMMARIES).substitute(
                region_id=region_id, tag=tag
            )
        )
        result = EAM.MarketOrderSummaries.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result
