"""File loaders for data sets."""

import json
import logging
from collections.abc import Iterable
from pathlib import Path
from string import Template
from time import perf_counter

from eve_argus.models import argus as EAM
from eve_argus.snippets.file.csv import write_dicts_to_csv
from eve_argus.snippets.file.validate_file_out import validate_file_out

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ArgusFilePaths:
    """File paths to Argus data files."""

    TYPE_INFO = Path("localized-type-info.json")
    TYPE_DESCRIPTION = Path("localized-type-descriptions.json")
    BLUEPRINTS = Path("blueprints.json")
    MARKET_GROUPS = Path("market-groups.json")
    META_GROUPS = Path("meta-groups.json")
    GROUPS = Path("groups.json")
    CATEGORIES = Path("categories.json")
    MARKET_PRICES_UNIVERSE = Path("market-prices-universe.json")
    ESI_DATA = Path("esi-data")
    TYPE_IDS_PUBLISHED = Path("type-ids-published.json")
    TYPE_IDS_IN_BLUEPRINTS = Path("type-ids-in-blueprints.json")
    TYPE_IDS_IN_MARKET = Path("type-ids-in-market.json")
    TYPE_IDS_FOR_INDUSTRY_PRICING = Path("type-ids-for-industry-pricing.json")
    SYSTEM_COST_INDICES = Path("system-cost-indices.json")
    # Template strings
    MARKET_HISTORY_BY_TYPE = "${region_id}-${type_id}-market-history.json"
    MARKET_HISTORY_BY_REGION = "${region_id}-market-history.json"
    MARKET_ORDERS_BY_REGION = "${region_id}-market-orders.json"
    MARKET_ORDERS_BY_TYPE = "${region_id}-${type_id}-market-orders.json"
    MARKET_HISTORY_SUMMARIES_BY_REGION = (
        "${region_id}-${tag}-market-history-summaries.json"
    )
    MARKET_ORDER_SUMMARIES_BY_REGION = "${region_id}-${tag}-market-order-summaries.json"


class ArgusFileReader:
    def __init__(self, argus_path: Path) -> None:
        """API to load Argus specific data files."""
        self.argus_path = argus_path

    def system_cost_indices(self) -> EAM.SystemCostIndices:
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
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.MARKET_PRICES_UNIVERSE
        result = EAM.UniverseMarketPrices.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def type_ids_published(self) -> EAM.TypeIDSubset:
        """Load type IDs that are published."""
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.TYPE_IDS_PUBLISHED
        result = EAM.TypeIDSubset.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def type_ids_in_blueprints(self) -> EAM.TypeIDSubset:
        """Load type IDs that are used in blueprints."""
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.TYPE_IDS_IN_BLUEPRINTS
        result = EAM.TypeIDSubset.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def type_ids_in_market(self) -> EAM.TypeIDSubset:
        """Load type IDs that are possible in the market."""
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.TYPE_IDS_IN_MARKET
        result = EAM.TypeIDSubset.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def type_ids_for_industry_pricing(self) -> EAM.TypeIDSubset:
        """Load type IDs that are needed for industry pricing."""
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.TYPE_IDS_FOR_INDUSTRY_PRICING
        result = EAM.TypeIDSubset.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_history_by_type(
        self, region_id: int, type_id: int
    ) -> EAM.MarketHistoryByType:
        """Load market history for a specific region and type."""
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_HISTORY_BY_TYPE).substitute(
                region_id=region_id, type_id=type_id
            )
        )
        result = EAM.MarketHistoryByType.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_history_by_region(self, region_id: int) -> EAM.MarketHistoryByRegion:
        """Load market history for a specific region."""
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_HISTORY_BY_REGION).substitute(
                region_id=region_id
            )
        )
        result = EAM.MarketHistoryByRegion.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_orders_by_region(self, region_id: int) -> EAM.MarketOrdersByRegion:
        """Load market orders for a specific region."""
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDERS_BY_REGION).substitute(
                region_id=region_id
            )
        )
        result = EAM.MarketOrdersByRegion.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_orders_by_region_and_type(
        self, region_id: int, type_id: int
    ) -> EAM.MarketOrdersByType:
        """Load market orders for a specific region and type."""
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDERS_BY_TYPE).substitute(
                region_id=region_id, type_id=type_id
            )
        )
        result = EAM.MarketOrdersByType.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_history_summaries_by_region(
        self, region_id: int, tag: str = "all"
    ) -> EAM.MarketHistorySummariesByRegion:
        """Load market order summaries for a specific region."""
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_HISTORY_SUMMARIES_BY_REGION).substitute(
                region_id=region_id, tag=tag
            )
        )
        result = EAM.MarketHistorySummariesByRegion.model_validate_json(
            path_in.read_text()
        )
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_order_summaries_by_region(
        self, region_id: int, tag: str = "all"
    ) -> EAM.MarketOrderSummaries:
        """Load market order summaries for a specific region."""
        start = perf_counter()
        path_in = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDER_SUMMARIES_BY_REGION).substitute(
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


class ArgusFileWriter:
    def __init__(self, argus_path: Path) -> None:
        """API to save Argus specific data files."""
        self.argus_path = argus_path

    def system_cost_indices_to_json(
        self, system_cost_indices: EAM.SystemCostIndices, overwrite: bool = True
    ) -> Path:
        """Save system cost indices to JSON."""
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.SYSTEM_COST_INDICES
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(system_cost_indices.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def type_info_to_csv(
        self, type_info: Iterable[EAM.TypeInfo], overwrite: bool = True
    ) -> tuple[int, Path]:
        """type_info_to_csv _summary_.

        Args:
            type_info (Iterable[EAM.TypeInfo]): _description_
            overwrite (bool, optional): _description_. Defaults to True.

        Returns:
            int: _description_
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_INFO.with_suffix(".csv")
        data = (EAM.TypeInfo.model_dump(x) for x in type_info)
        count = write_dicts_to_csv(data=data, file_path=path_out, overwrite=overwrite)
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return (count, path_out)

    def type_info_to_json(
        self, type_info: Iterable[EAM.TypeInfo], overwrite: bool = True
    ) -> Path:
        """type_info_to_json _summary_.

        Args:
            type_info (Iterable[EAM.TypeInfo]): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_INFO
        data = {x.type_id: x for x in type_info}
        data_dict = EAM.TypeInfos(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def type_description_to_csv(
        self, type_description: Iterable[EAM.TypeDescription], overwrite: bool = True
    ) -> tuple[int, Path]:
        """type_description_to_csv _summary_.

        Args:
            type_description (Iterable[EAM.TypeDescription]): _description_
            overwrite (bool, optional): _description_. Defaults to True.

        Returns:
            int: _description_
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_DESCRIPTION.with_suffix(".csv")
        data = (EAM.TypeDescription.model_dump(x) for x in type_description)
        count = write_dicts_to_csv(data=data, file_path=path_out, overwrite=overwrite)
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return (count, path_out)

    def type_description_to_json(
        self, type_description: Iterable[EAM.TypeDescription], overwrite: bool = True
    ) -> Path:
        """type_description_to_json _summary_.

        Args:
            type_description (Iterable[EAM.TypeDescription]): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_DESCRIPTION
        data = {x.type_id: x for x in type_description}
        data_dict = EAM.TypeDescriptions(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def blueprints_to_json(
        self, blueprints: Iterable[EAM.Blueprint], overwrite: bool = True
    ) -> Path:
        """blueprints_to_json _summary_.

        Args:
            blueprints (Iterable[EAM.Blueprint]): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        # TODO does json automatically force keys to be str?
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.BLUEPRINTS
        data = {x.blueprintTypeID: x for x in blueprints}
        data_dict = EAM.Blueprints(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_groups_to_json(
        self, market_groups: Iterable[EAM.MarketGroup], overwrite: bool = True
    ) -> Path:
        """market_groups_to_json.

        Args:
            market_groups (Iterable[EAM.MarketGroup]): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.MARKET_GROUPS
        data = {x.group_id: x for x in market_groups}
        data_dict = EAM.MarketGroups(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def meta_groups_to_json(
        self, meta_groups: Iterable[EAM.MetaGroup], overwrite: bool = True
    ) -> Path:
        """meta_groups_to_json.

        Args:
            meta_groups (Iterable[EAM.MetaGroup]): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.META_GROUPS
        data = {x.meta_id: x for x in meta_groups}
        data_dict = EAM.MetaGroups(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def groups_to_json(
        self, groups: Iterable[EAM.Group], overwrite: bool = True
    ) -> Path:
        """groups_to_json.

        Args:
            groups (Iterable[EAM.Group]): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.GROUPS
        data = {x.group_id: x for x in groups}
        data_dict = EAM.Groups(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def categories_to_json(
        self, categories: Iterable[EAM.Category], overwrite: bool = True
    ) -> Path:
        """categories_to_json.

        Args:
            categories (Iterable[EAM.Category]): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.CATEGORIES
        data = {x.category_id: x for x in categories}
        data_dict = EAM.Categories(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    # TODO standardized file out formats, dicts or list?
    def market_prices_universe_to_json(
        self, market_prices: Iterable[EAM.UniverseMarketPrice], overwrite: bool = True
    ) -> Path:
        """market_prices_universe_to_json.

        Args:
            market_prices (Iterable[EAM.MarketPricesUniverse]): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        start = perf_counter()
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / ArgusFilePaths.MARKET_PRICES_UNIVERSE
        )
        data = {x.type_id: x for x in market_prices}
        data_dict = EAM.UniverseMarketPrices(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_history_by_type_to_json(
        self,
        region_id: int,
        type_id: int,
        market_history: EAM.MarketHistoryByType,
        overwrite: bool = True,
    ) -> Path:
        """market_history_to_json.

        Args:
            market_history (EAM.MarketHistoryDict): _description_
            region_id (int): _description_
            type_id (int): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        start = perf_counter()
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_HISTORY_BY_TYPE).substitute(
                region_id=region_id, type_id=type_id
            )
        )

        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_history.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_history_by_region_to_json(
        self,
        market_history: EAM.MarketHistoryByRegion,
        overwrite: bool = True,
    ) -> Path:
        """market_history_by_region_to_json."""
        start = perf_counter()
        region_id = market_history.region_id
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_HISTORY_BY_REGION).substitute(
                region_id=region_id
            )
        )

        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_history.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def region_market_types_to_json(
        self,
        region_market_types: Iterable[int],
        region_id: int,
        overwrite: bool = True,
    ):
        """region_market_types_to_json."""
        # TODO change this to type_ids: EAM.TypeIDSubset
        start = perf_counter()
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / f"{region_id}-region-market-types.json"
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        data = {"region_id": region_id, "type_ids": list(region_market_types)}
        path_out.write_text(json.dumps(data, indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_orders_by_region_to_json(
        self,
        market_orders_by_region: EAM.MarketOrdersByRegion,
        overwrite: bool = True,
    ):
        """market_orders_to_json."""
        start = perf_counter()
        region_id = market_orders_by_region.region_id
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDERS_BY_REGION).substitute(
                region_id=region_id
            )
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_orders_by_region.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_orders_by_region_and_type_to_json(
        self,
        market_orders_by_type: EAM.MarketOrdersByType,
        overwrite: bool = True,
    ) -> Path:
        """market_orders_by_region_and_type_to_json."""
        start = perf_counter()
        region_id = market_orders_by_type.region_id
        type_id = market_orders_by_type.type_id
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDERS_BY_TYPE).substitute(
                region_id=region_id, type_id=type_id
            )
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_orders_by_type.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def type_ids_published_to_json(
        self, type_ids: EAM.TypeIDSubset, overwrite: bool = True
    ) -> Path:
        """type_ids_published_to_json."""
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_IDS_PUBLISHED
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(type_ids.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def type_ids_in_blueprints_to_json(
        self, type_ids: EAM.TypeIDSubset, overwrite: bool = True
    ) -> Path:
        """type_ids_in_blueprints_to_json."""
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_IDS_IN_BLUEPRINTS
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(type_ids.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def type_ids_in_market_to_json(
        self, type_ids: EAM.TypeIDSubset, overwrite: bool = True
    ) -> Path:
        """type_ids_in_market_to_json."""
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_IDS_IN_MARKET
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(type_ids.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def type_ids_for_industry_pricing_to_json(
        self, type_ids: EAM.TypeIDSubset, overwrite: bool = True
    ) -> Path:
        """type_ids_for_industry_pricing_to_json."""
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.TYPE_IDS_FOR_INDUSTRY_PRICING
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(type_ids.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_history_summaries_by_region_to_json(
        self,
        market_history_summaries: EAM.MarketHistorySummariesByRegion,
        tag: str = "all",
        overwrite: bool = True,
    ) -> Path:
        """market_history_summaries_by_region_to_json."""
        start = perf_counter()
        region_id = market_history_summaries.region_id
        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_HISTORY_SUMMARIES_BY_REGION).substitute(
                region_id=region_id, tag=tag
            )
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_history_summaries.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_order_summaries_by_region_to_json(
        self,
        market_order_summaries: EAM.MarketOrderSummaries,
        region_id: int,
        tag: str = "all",
        overwrite: bool = True,
    ) -> Path:
        """Save market order summaries for a specific region to JSON."""
        start = perf_counter()

        path_out = (
            self.argus_path
            / ArgusFilePaths.ESI_DATA
            / Template(ArgusFilePaths.MARKET_ORDER_SUMMARIES_BY_REGION).substitute(
                region_id=region_id, tag=tag
            )
        )
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(market_order_summaries.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out
