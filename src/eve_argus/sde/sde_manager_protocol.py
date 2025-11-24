"""Agrus static data manager protocol definition."""

from pathlib import Path
from typing import Protocol, Self

from eve_argus.models import static_data as SD


class SdeManagerProtocol(Protocol):
    @classmethod
    def import_data(cls, source: Path, destination: Path) -> Self:
        """Import static data from the given source path into the SDE manager.

        Args:
            source (Path): The path to the source data to import.
            destination (Path): The path to the destination for imported data.

        Returns:
            Self: An instance of the SDE manager with imported data.
        """
        ...

    def status(self) -> SD.SdeInfo | None:
        """Retrieve information about the current SDE.

        Returns:
            SD.SdeInfo | None: An object containing SDE information, or None if no SDE is loaded.
        """
        ...

    @property
    def blueprints(self) -> SD.Blueprints:
        """Retrieve the blueprints data from the SDE.

        Returns:
            SD.Blueprints: An object containing blueprints data.
        """
        ...

    @property
    def categories(self) -> SD.Categories:
        """Retrieve the categories data from the SDE.

        Returns:
            SD.Categories: An object containing categories data.
        """
        ...

    @property
    def groups(self) -> SD.Groups:
        """Retrieve the groups data from the SDE.

        Returns:
            SD.Groups: An object containing groups data.
        """
        ...

    @property
    def meta_groups(self) -> SD.MetaGroups:
        """Retrieve the meta groups data from the SDE.

        Returns:
            SD.MetaGroups: An object containing meta groups data.
        """
        ...

    @property
    def type_materials(self) -> SD.TypeMaterials:
        """Retrieve the type materials data from the SDE.

        Returns:
            SD.TypeMaterials: An object containing type materials data.
        """
        ...

    @property
    def eve_types(self) -> SD.EveTypes:
        """Retrieve the Eve types data from the SDE.

        Returns:
            SD.EveTypes: An object containing Eve types data.
        """
        ...

    @property
    def regions(self) -> SD.Regions:
        """Retrieve the regions data from the SDE.

        Returns:
            SD.Regions: An object containing regions data.
        """
        ...
