"""Code to manage SDE data stored in JSON format."""

from enum import StrEnum
from pathlib import Path
from typing import Self

from eve_static_data.raw_jsonl_access import RawJsonFileAccess

from eve_argus.models import static_data as SD

from .sde_manager_protocol import SdeManagerProtocol


class ArgusSdeFiles(StrEnum):
    SDE_INFO = "sde_info.json"
    BLUEPRINTS = "blueprints.json"
    CATEGORIES = "categories.json"
    GROUPS = "groups.json"
    META_GROUPS = "metagroups.json"
    TYPE_MATERIALS = "type_materials.json"
    EVE_TYPES = "eve_types.json"
    REGIONS = "regions.json"
    MARKET_GROUPS = "market_groups.json"


class SdeManagerJSON(SdeManagerProtocol):
    def __init__(self, store_path: Path) -> None:
        """Initialize the SDE Manager with JSON file storage.

        Args:
            store_path (Path): The path to the directory where SDE JSON files are stored.

        SdeManagerJSON provides access to static data stored in JSON format files.
        These files are lazy loaded upon first access.

        Missing files will raise FileNotFoundError when accessed.

        Use SdeManagerJSON.status() to retrieve SDE information, and check if the store_path
        contains valid SDE data. Will return None if no SDE info file is found.

        Use SdeManagerJSON.import_data to import data from a source directory.


        """
        self.store_path = store_path
        self._sde_info: SD.SdeInfo | None = None
        self._blueprints: SD.Blueprints | None = None
        self._categories: SD.Categories | None = None
        self._groups: SD.Groups | None = None
        self._meta_groups: SD.MetaGroups | None = None
        self._type_materials: SD.TypeMaterials | None = None
        self._eve_types: SD.EveTypes | None = None
        self._regions: SD.Regions | None = None
        self._market_groups: SD.MarketGroups | None = None

    @classmethod
    def import_data(cls, source: Path, destination: Path) -> Self:
        """Import SDE data from a source directory to a destination directory.

        This method creates an SdeImportJson instance to handle the import process,
        executes the import for all data types, and returns a new instance of the
        class initialized with the destination path.

        Args:
            source (Path): The source directory path containing the SDE data to import.
            destination (Path): The destination directory path where the imported data will be stored.

        Returns:
            Self: A new instance of the class initialized with the destination path.

        Example:
            >>> manager = SdeManager.import_data(
            ...     source=Path("/path/to/sde/source"), destination=Path("/path/to/sde/destination")
            ... )
        """
        importer = SdeImportJson(source=source, destination=destination)
        importer.all()
        return cls(destination)

    def status(self) -> SD.SdeInfo | None:
        return self._sde_info

    @property
    def blueprints(self) -> SD.Blueprints:
        if self._blueprints is None:
            blueprint_file = self.store_path / ArgusSdeFiles.BLUEPRINTS
            if not blueprint_file.exists():
                raise FileNotFoundError(f"Blueprints file not found: {blueprint_file}")
            self._blueprints = SD.Blueprints.load_from_disk(blueprint_file)
        return self._blueprints

    @property
    def categories(self) -> SD.Categories:
        if self._categories is None:
            categories_file = self.store_path / ArgusSdeFiles.CATEGORIES
            if not categories_file.exists():
                raise FileNotFoundError(f"Categories file not found: {categories_file}")
            self._categories = SD.Categories.load_from_disk(categories_file)
        return self._categories

    @property
    def groups(self) -> SD.Groups:
        if self._groups is None:
            groups_file = self.store_path / ArgusSdeFiles.GROUPS
            if not groups_file.exists():
                raise FileNotFoundError(f"Groups file not found: {groups_file}")
            self._groups = SD.Groups.load_from_disk(groups_file)
        return self._groups

    @property
    def meta_groups(self) -> SD.MetaGroups:
        if self._meta_groups is None:
            meta_groups_file = self.store_path / ArgusSdeFiles.META_GROUPS
            if not meta_groups_file.exists():
                raise FileNotFoundError(
                    f"Meta groups file not found: {meta_groups_file}"
                )
            self._meta_groups = SD.MetaGroups.load_from_disk(meta_groups_file)
        return self._meta_groups

    @property
    def type_materials(self) -> SD.TypeMaterials:
        if self._type_materials is None:
            type_materials_file = self.store_path / ArgusSdeFiles.TYPE_MATERIALS
            if not type_materials_file.exists():
                raise FileNotFoundError(
                    f"Type materials file not found: {type_materials_file}"
                )
            self._type_materials = SD.TypeMaterials.load_from_disk(type_materials_file)
        return self._type_materials


class SdeImportJson:
    def __init__(self, source: Path, destination: Path) -> None:
        """Initialize the SDE Manager with source and destination paths.

        Args:
            source (Path): The path to the source directory containing SDE JSON files.
            destination (Path): The path to the destination directory for processed data.

        Returns:
            None
        """
        self.source = source
        self.destination = destination
        self.access = RawJsonFileAccess(source)

    def all(self, localized: str = "en", only_published: bool = True) -> None:
        self.sde_info()
        self.blueprints(only_published=only_published)
        self.categories(localized=localized, only_published=only_published)
        self.groups(localized=localized, only_published=only_published)
        self.meta_groups(localized=localized)
        self.type_materials()
        self.eve_types(localized=localized, only_published=only_published)
        self.market_groups(localized=localized)
        self.regions(localized=localized)

    def blueprints(self, only_published: bool = True) -> None:
        blueprints = SD.Blueprints.from_sap(
            access=self.access, only_published=only_published
        )
        file_out = self.destination / ArgusSdeFiles.BLUEPRINTS
        blueprints.save_to_disk(file_out, overwrite=True)

    def sde_info(self) -> None:
        sde_info = SD.SdeInfo.from_sap(access=self.access)
        file_out = self.destination / ArgusSdeFiles.SDE_INFO
        sde_info.save_to_disk(file_out, overwrite=True)

    def regions(self, localized: str = "en") -> None:
        regions = SD.Regions.from_sap(access=self.access, localized=localized)
        file_out = self.destination / ArgusSdeFiles.REGIONS
        regions.save_to_disk(file_out, overwrite=True)

    def categories(self, localized: str = "en", only_published: bool = True) -> None:
        categories = SD.Categories.from_sap(
            access=self.access, localized=localized, only_published=only_published
        )
        file_out = self.destination / ArgusSdeFiles.CATEGORIES
        categories.save_to_disk(file_out, overwrite=True)

    def groups(self, localized: str = "en", only_published: bool = True) -> None:
        groups = SD.Groups.from_sap(
            access=self.access, localized=localized, only_published=only_published
        )
        file_out = self.destination / ArgusSdeFiles.GROUPS
        groups.save_to_disk(file_out, overwrite=True)

    def meta_groups(self, localized: str = "en", only_published: bool = True) -> None:
        meta_groups = SD.MetaGroups.from_sap(access=self.access, localized=localized)
        file_out = self.destination / ArgusSdeFiles.META_GROUPS
        meta_groups.save_to_disk(file_out, overwrite=True)

    def type_materials(self) -> None:
        type_materials = SD.TypeMaterials.from_sap(access=self.access)
        file_out = self.destination / ArgusSdeFiles.TYPE_MATERIALS
        type_materials.save_to_disk(file_out, overwrite=True)

    def eve_types(
        self,
        localized: str = "en",
        only_published: bool = True,
    ) -> None:
        eve_types = SD.EveTypes.from_sap(
            access=self.access, localized=localized, only_published=only_published
        )
        file_out = self.destination / ArgusSdeFiles.EVE_TYPES
        eve_types.save_to_disk(file_out, overwrite=True)

    def market_groups(self, localized: str = "en") -> None:
        market_groups = SD.MarketGroups.from_sap(
            access=self.access, localized=localized
        )
        file_out = self.destination / ArgusSdeFiles.MARKET_GROUPS
        market_groups.save_to_disk(file_out, overwrite=True)
