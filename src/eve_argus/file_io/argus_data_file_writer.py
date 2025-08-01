"""argus_data_file_writer.py.

This module provides functionality to write Argus data files in JSON format.
"""

import logging
from pathlib import Path
from string import Template
from time import perf_counter

from eve_argus.file_io.argus_file_paths import ArgusFilePaths
from eve_argus.models import argus as EAM
from eve_argus.snippets.file.validate_file_out import validate_file_out

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ArgusFileWriter:
    def __init__(self, argus_path: Path) -> None:
        """API to save Argus specific data files."""
        self.argus_path = argus_path

    def system_cost_indices(
        self, system_cost_indices: EAM.SystemCostIndices, overwrite: bool = True
    ) -> Path:
        """Save system cost indices to JSON.

        Args:
            system_cost_indices (EAM.SystemCostIndices): The system cost indices to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.SYSTEM_COST_INDICES
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(system_cost_indices.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def type_infos(self, type_infos: EAM.TypeInfos, overwrite: bool = True) -> Path:
        """Save type information to JSON.

        Args:
            type_infos (EAM.TypeInfos): The type information to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_INFO
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(type_infos.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def type_descriptions(
        self, type_descriptions: EAM.TypeDescriptions, overwrite: bool = True
    ) -> Path:
        """Save type descriptions to JSON.

        Args:
            type_descriptions (EAM.TypeDescriptions): The type descriptions to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_DESCRIPTION

        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(type_descriptions.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def blueprints(self, blueprints: EAM.Blueprints, overwrite: bool = True) -> Path:
        """Save blueprints to JSON.

        Args:
            blueprints (EAM.Blueprints): The blueprints to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.BLUEPRINTS

        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(blueprints.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_groups(
        self, market_groups: EAM.MarketGroups, overwrite: bool = True
    ) -> Path:
        """Save market groups to JSON.

        Args:
            market_groups (EAM.MarketGroups): The market groups to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.MARKET_GROUPS
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_groups.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def meta_groups(self, meta_groups: EAM.MetaGroups, overwrite: bool = True) -> Path:
        """Save meta groups to JSON.

        Args:
            meta_groups (EAM.MetaGroups): The meta groups to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.META_GROUPS
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(meta_groups.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def groups(self, groups: EAM.Groups, overwrite: bool = True) -> Path:
        """Save groups to JSON.

        Args:
            groups (EAM.Groups): The groups to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.GROUPS
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(groups.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def categories(self, categories: EAM.Categories, overwrite: bool = True) -> Path:
        """Save categories to JSON.

        Args:
            categories (EAM.Categories): The categories to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.CATEGORIES

        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(categories.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def universe_market_prices(
        self, market_prices: EAM.UniverseMarketPrices, overwrite: bool = True
    ) -> Path:
        """Save market prices for the entire universe to JSON.

        Args:
            market_prices (EAM.UniverseMarketPrices): The market prices data to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.
        """
        start = perf_counter()
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / ArgusFilePaths.MARKET_PRICES_UNIVERSE
        )

        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_prices.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def type_id_subsets(
        self, type_id_subsets: EAM.TypeIDSubsets, overwrite: bool = True
    ) -> Path:
        """Save type ID subsets to JSON.

        Args:
            type_id_subsets (EAM.TypeIDSubsets): The type ID subsets to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_ID_SUBSETS
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(type_id_subsets.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    # def market_history(
    #     self,
    #     region_id: int,
    #     type_id: int,
    #     market_history: EAM.MarketHistory,
    #     overwrite: bool = True,
    # ) -> Path:
    #     """Save market history for a specific region and type to JSON.

    #     Args:
    #         region_id (int): The ID of the region.
    #         type_id (int): The ID of the type.
    #         market_history (EAM.MarketHistory): The market history data to save.
    #         overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

    #     Returns:
    #         Path: The path to the saved JSON file.
    #     """
    #     start = perf_counter()
    #     path_out = (
    #         self.argus_path
    #         / ArgusFilePaths.ESI_DATA
    #         / Template(ArgusFilePaths.MARKET_HISTORY).substitute(
    #             region_id=region_id, type_id=type_id
    #         )
    #     )

    #     validate_file_out(file_path=path_out, overwrite=overwrite)
    #     path_out.write_text(market_history.model_dump_json(indent=2))
    #     logger.info(
    #         "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
    #     )
    #     return path_out

    # def market_histories(
    #     self,
    #     market_history: EAM.MarketHistories,
    #     overwrite: bool = True,
    # ) -> Path:
    #     """Save regional market history to JSON.

    #     Args:
    #         market_history (EAM.RegionalMarketHistory): The regional market history data to save.
    #         overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

    #     Returns:
    #         Path: The path to the saved JSON file.
    #     """
    #     start = perf_counter()
    #     region_id = market_history.region_id
    #     path_out = (
    #         self.argus_path
    #         / ArgusFilePaths.ESI_DATA
    #         / Template(ArgusFilePaths.MARKET_HISTORIES).substitute(region_id=region_id)
    #     )

    #     validate_file_out(file_path=path_out, overwrite=overwrite)
    #     path_out.write_text(market_history.model_dump_json(indent=2))
    #     logger.info(
    #         "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
    #     )
    #     return path_out

    def region_market_types(
        self,
        region_market_types: EAM.TypeIDSubset,
        region_id: int,
        overwrite: bool = True,
    ):
        """Save region market types to JSON.

        Args:
            region_market_types (EAM.TypeIDSubset): The region market types data to save.
            region_id (int): The ID of the region.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / f"{region_id}-region-market-types.json"
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(region_market_types.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def regional_market_orders(
        self,
        regional_market_orders: EAM.RegionalMarketOrders,
        overwrite: bool = True,
    ):
        """Save market orders by region to JSON.

        Args:
            regional_market_orders (EAM.RegionalMarketOrders): The regional market orders data to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        region_id = regional_market_orders.region_id
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.REGIONAL_MARKET_ORDERS).substitute(
                region_id=region_id
            )
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(regional_market_orders.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_orders(
        self,
        market_orders: EAM.MarketOrders,
        overwrite: bool = True,
    ) -> Path:
        """Save market orders of one type and one region to JSON.

        Args:
            market_orders (EAM.MarketOrders): The market orders data to save.
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        region_id = market_orders.region_id
        type_id = market_orders.type_id
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDERS).substitute(
                region_id=region_id, type_id=type_id
            )
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_orders.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    # def type_ids_published(
    #     self, type_ids: EAM.TypeIDSubset, overwrite: bool = True
    # ) -> Path:
    #     """Save type IDs that are published to JSON.

    #     Args:
    #         type_ids (EAM.TypeIDSubset): The type IDs to save.
    #         overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

    #     Returns:
    #         Path: The path to the saved JSON file.
    #     """
    #     start = perf_counter()
    #     path_out = self.argus_path / ArgusFilePaths.TYPE_IDS_PUBLISHED
    #     validate_file_out(file_path=path_out, overwrite=overwrite)
    #     path_out.write_text(type_ids.model_dump_json(indent=2))
    #     logger.info(
    #         "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
    #     )
    #     return path_out

    # def type_ids_in_blueprints(
    #     self, type_ids: EAM.TypeIDSubset, overwrite: bool = True
    # ) -> Path:
    #     """Save type IDs in blueprints to JSON.

    #     Args:
    #         type_ids (EAM.TypeIDSubset): The type IDs to save.
    #         overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

    #     Returns:
    #         Path: The path to the saved JSON file.
    #     """
    #     start = perf_counter()
    #     path_out = self.argus_path / ArgusFilePaths.TYPE_IDS_IN_BLUEPRINTS
    #     validate_file_out(file_path=path_out, overwrite=overwrite)
    #     path_out.write_text(type_ids.model_dump_json(indent=2))
    #     logger.info(
    #         "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
    #     )
    #     return path_out

    # def type_ids_in_market(
    #     self, type_ids: EAM.TypeIDSubset, overwrite: bool = True
    # ) -> Path:
    #     """Save type IDs in market to JSON.

    #     Args:
    #         type_ids (EAM.TypeIDSubset): The type IDs to save.
    #         overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

    #     Returns:
    #         Path: The path to the saved JSON file.
    #     """
    #     start = perf_counter()
    #     path_out = self.argus_path / ArgusFilePaths.TYPE_IDS_IN_MARKET
    #     validate_file_out(file_path=path_out, overwrite=overwrite)
    #     path_out.write_text(type_ids.model_dump_json(indent=2))
    #     logger.info(
    #         "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
    #     )
    #     return path_out

    # def type_ids_for_industry_pricing(
    #     self, type_ids: EAM.TypeIDSubset, overwrite: bool = True
    # ) -> Path:
    #     """Save type IDs for industry pricing to JSON.

    #     Args:
    #         type_ids (EAM.TypeIDSubset): The type IDs to save.
    #         overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

    #     Returns:
    #         Path: The path to the saved JSON file.
    #     """
    #     start = perf_counter()
    #     path_out = self.argus_path / ArgusFilePaths.TYPE_IDS_FOR_INDUSTRY_PRICING
    #     validate_file_out(file_path=path_out, overwrite=overwrite)
    #     path_out.write_text(type_ids.model_dump_json(indent=2))
    #     logger.info(
    #         "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
    #     )
    #     return path_out

    def market_history_summaries(
        self,
        market_history_summaries: EAM.MarketHistorySummaries,
        tag: str = "all",
        overwrite: bool = True,
    ) -> Path:
        """Save market history summaries by region to JSON.

        Args:
            market_history_summaries (EAM.MarketHistorySummariesByRegion): The market history summaries data to save.
            tag (str, optional): A tag to append to the filename. Defaults to "all".
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()
        region_id = market_history_summaries.region_id
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_HISTORY_SUMMARIES).substitute(
                region_id=region_id, tag=tag
            )
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_history_summaries.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_order_summaries(
        self,
        market_order_summaries: EAM.MarketOrderSummaries,
        region_id: int,
        tag: str = "all",
        overwrite: bool = True,
    ) -> Path:
        """Save market order summaries by region to JSON.

        Args:
            market_order_summaries (EAM.MarketOrderSummaries): The market order summaries data to save.
            region_id (int): The ID of the region.
            tag (str, optional): A tag to append to the filename. Defaults to "all".
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to True.

        Returns:
            Path: The path to the saved JSON file.
        """
        start = perf_counter()

        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDER_SUMMARIES).substitute(
                region_id=region_id, tag=tag
            )
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_order_summaries.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out


# FIXME refactor typeidsubset, unused markethistory.
