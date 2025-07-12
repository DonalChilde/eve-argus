"""File loaders for data sets."""

from collections.abc import Iterable
from pathlib import Path
from time import perf_counter
from typing import Any
from yaml import safe_load
from eve_argus.models import argus as EAM
from eve_argus.snippets.file.csv import write_dicts_to_csv
import json
from eve_argus.snippets.file.validate_file_out import validate_file_out
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SdeFilePaths:
    TYPES = Path("fsd") / "types.yaml"
    BLUEPRINTS = Path("fsd") / "blueprints.yaml"
    MARKET_GROUPS = Path("fsd") / "marketGroups.yaml"
    META_GROUPS = Path("fsd") / "metaGroups.yaml"
    GROUPS = Path("fsd") / "groups.yaml"
    CATEGORIES = Path("fsd") / "categories.yaml"


class SdeLoader:
    def __init__(self, sde_path: Path) -> None:
        """API to load files from the sde.

        Args:
            sde_path (Path): _description_
        """
        self.sde_path = sde_path

    def load_types(self) -> dict[int, dict[str, Any]]:
        """Load type info from the sde.

        Returns:
            dict[int, dict[str, Any]]: _description_
        """
        path_in = self.sde_path / SdeFilePaths.TYPES
        with open(path_in) as file_in:
            data = safe_load(file_in)
        return data

    def load_blueprints(self) -> dict[int, dict[str, Any]]:
        """Load blueprints from the sde.

        Returns:
            dict[int, dict[str, Any]]: _description_
        """
        path_in = self.sde_path / SdeFilePaths.BLUEPRINTS
        with open(path_in) as file_in:
            data = safe_load(file_in)
        return data

    def load_market_groups(self) -> dict[int, dict[str, Any]]:
        """Load market groups from sde.

        Returns:
            dict[int, dict[str, Any]]: _description_
        """
        path_in = self.sde_path / SdeFilePaths.MARKET_GROUPS
        with open(path_in) as file_in:
            data = safe_load(file_in)
        return data

    def load_meta_groups(self) -> dict[int, dict[str, Any]]:
        path_in = self.sde_path / SdeFilePaths.META_GROUPS
        with open(path_in) as file_in:
            data = safe_load(file_in)
        return data

    def load_groups(self) -> dict[int, dict[str, Any]]:
        path_in = self.sde_path / SdeFilePaths.GROUPS
        with open(path_in) as file_in:
            data = safe_load(file_in)
        return data

    def load_categories(self) -> dict[int, dict[str, Any]]:
        path_in = self.sde_path / SdeFilePaths.CATEGORIES
        with open(path_in) as file_in:
            data = safe_load(file_in)
        return data


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


class ArgusLoader:
    def __init__(self, argus_path: Path) -> None:
        """API to load Argus specific data files."""
        self.argus_path = argus_path

    def type_info(self) -> EAM.TypeInfoDict:
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.TYPE_INFO
        result = EAM.TypeInfoDict.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def type_description(self) -> EAM.TypeDescriptionDict:
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.TYPE_DESCRIPTION
        result = EAM.TypeDescriptionDict.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def blueprints(self) -> EAM.BlueprintsDict:
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.BLUEPRINTS
        result = EAM.BlueprintsDict.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_groups(self) -> EAM.MarketGroupDict:
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.MARKET_GROUPS
        result = EAM.MarketGroupDict.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def meta_groups(self) -> EAM.MetaGroupDict:
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.META_GROUPS
        result = EAM.MetaGroupDict.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def groups(self) -> EAM.GroupDict:
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.GROUPS
        result = EAM.GroupDict.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def categories(self) -> EAM.CategoryDict:
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.CATEGORIES
        result = EAM.CategoryDict.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result

    def market_prices_universe(self) -> EAM.MarketPricesUniverseDict:
        start = perf_counter()
        path_in = self.argus_path / ArgusFilePaths.MARKET_PRICES_UNIVERSE
        result = EAM.MarketPricesUniverseDict.model_validate_json(path_in.read_text())
        logger.info(
            "Loaded data from %s in %s seconds",
            path_in,
            f"{perf_counter() - start:.6f}",
        )
        return result


class ArgusWriter:
    def __init__(self, argus_path: Path) -> None:
        """API to save Argus specific data files."""
        self.argus_path = argus_path

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
        data_dict = EAM.TypeInfoDict(data=data)
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
        data_dict = EAM.TypeDescriptionDict(data=data)
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
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.BLUEPRINTS
        data = {x.blueprint_type_id: x for x in blueprints}
        data_dict = EAM.BlueprintsDict(data=data)
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
        data_dict = EAM.MarketGroupDict(data=data)
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
        data_dict = EAM.MetaGroupDict(data=data)
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
        data_dict = EAM.GroupDict(data=data)
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
        data_dict = EAM.CategoryDict(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out

    def market_prices_universe_to_json(
        self, market_prices: Iterable[EAM.MarketPricesUniverse], overwrite: bool = True
    ) -> Path:
        """market_prices_universe_to_json.

        Args:
            market_prices (Iterable[EAM.MarketPricesUniverse]): _description_
            overwrite (bool, optional): _description_. Defaults to True.
        """
        start = perf_counter()
        path_out = self.argus_path / ArgusFilePaths.MARKET_PRICES_UNIVERSE
        data = {x.type_id: x for x in market_prices}
        data_dict = EAM.MarketPricesUniverseDict(data=data)
        validate_file_out(file_path=path_out, overwrite=overwrite)
        path_out.write_text(data_dict.model_dump_json(indent=2))
        logger.info(
            "Saved data to %s in %s seconds", path_out, f"{perf_counter() - start:.6f}"
        )
        return path_out
