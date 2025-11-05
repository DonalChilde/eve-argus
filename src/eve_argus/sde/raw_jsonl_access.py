import json
from collections.abc import Iterable
from enum import StrEnum
from pathlib import Path
from typing import Any

from eve_argus.helpers.jsonl_reader import read_jsonl_dicts
from eve_argus.sde.sde_access_protocol import SdeAccessProtocol


class SdeFileNames(StrEnum):
    SDE_INFO = "_sde.jsonl"
    BLUEPRINTS = "blueprints.jsonl"
    MARKET_GROUPS = "marketGroups.jsonl"
    TYPES = "types.jsonl"


class RawJsonAccess(SdeAccessProtocol):
    def __init__(self, sde_directory: Path) -> None:
        self.sde_directory = sde_directory

    def jsonl_iter(self, sde_file: SdeFileNames) -> Iterable[dict[str, Any]]:
        """Get an iterator over the JSON objects in a JSONL SDE file.

        Args:
            sde_file: The SDE file to read.

        Returns:
            An iterator over the JSON objects in the file.
        """
        file_path = self.sde_directory / sde_file
        if not file_path.exists():
            raise FileNotFoundError(f"SDE file not found at {file_path}")
        return read_jsonl_dicts(file_path)

    def build_number(self) -> int:
        """Get the SDE build number.

        Returns:
            The SDE build number as an integer.
        """
        info = next(iter(self.jsonl_iter(SdeFileNames.SDE_INFO)))
        build_number = info.get("buildNumber")
        if build_number is None:
            raise ValueError("Build number not found in SDE info file")
        return int(build_number)

    def blueprints(self) -> Iterable[dict[str, Any]]:
        """Get an iterator over the blueprints in the SDE.

        Returns:
            An iterator over the blueprint JSON objects.
        """
        return self.jsonl_iter(SdeFileNames.BLUEPRINTS)

    def sde_info(self) -> dict:
        """Get the SDE info as a dictionary."""
        info = next(iter(self.jsonl_iter(SdeFileNames.SDE_INFO)))
        return info
