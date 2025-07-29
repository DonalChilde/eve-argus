"""Entry point for SDE data imports."""

import logging
from enum import StrEnum
from pathlib import Path
from typing import Any

from yaml import safe_load

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SdeFilePaths:
    TYPES = Path("fsd") / "types.yaml"
    BLUEPRINTS = Path("fsd") / "blueprints.yaml"
    MARKET_GROUPS = Path("fsd") / "marketGroups.yaml"
    META_GROUPS = Path("fsd") / "metaGroups.yaml"
    GROUPS = Path("fsd") / "groups.yaml"
    CATEGORIES = Path("fsd") / "categories.yaml"


class SdeSpecifiers(StrEnum):
    ALL = "all"
    TYPES = "types"
    BLUEPRINTS = "blueprints"
    MARKET_GROUPS = "market_groups"
    META_GROUPS = "meta_groups"
    GROUPS = "groups"
    CATEGORIES = "categories"


class SdeReader:
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
