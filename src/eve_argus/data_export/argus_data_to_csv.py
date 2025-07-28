"""Fuctions to write Argus data to CSV files."""

import logging
from collections.abc import Iterable
from pathlib import Path
from time import perf_counter

from eve_argus.config.argus_file_paths import ArgusFilePaths
from eve_argus.models import argus as EAM
from eve_argus.snippets.file.csv import write_dicts_to_csv

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ArgusCSVWriter:
    """Class to write Argus data to CSV files."""

    def __init__(self, argus_path: Path) -> None:
        """Initialize the ArgusCSVWriter with the path to the Argus data directory."""
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
