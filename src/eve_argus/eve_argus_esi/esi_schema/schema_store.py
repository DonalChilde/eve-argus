"""SchemaStore module for managing the ESI OpenAPI schema.

This module provides the SchemaStore class, which supports downloading, saving, and loading
the Eve Online ESI OpenAPI schema. It ensures schema validity and tracks metadata such as
download date and schema UUID.

Classes:
    SchemaStoreData: Pydantic model for schema metadata and content.
    SchemaStore: Main class for schema management.

Typical usage example:
    store = SchemaStore(file_path=Path('schema.json'))
    schema = store.esi_schema
    store.update()
"""

import json
import logging
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel

from eve_argus.eve_argus_esi.helpers.download_file import download_text
from eve_argus.eve_argus_esi.helpers.now_utc import now_utc

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SchemaStoreData(BaseModel):
    """Pydantic model for storing ESI schema metadata and content.

    Attributes:
        id_ (UUID): Unique identifier for the schema.
        download_date (str): ISO 8601 UTC download date.
        schema_ (dict[str, Any]): The ESI OpenAPI schema as a dictionary.
    """

    id_: UUID
    download_date: str
    schema_: dict[str, Any]


class SchemaStore:
    """Manages the ESI OpenAPI schema: download, save, load, and update.

    Attributes:
        _file_path (Path | None): Path to schema file, if used.
        _schema_url (str): URL to download schema from.
        _store_data (SchemaStoreData | None): Loaded schema data and metadata.

    Raises:
        ValueError: On invalid schema, missing file, or failed operations.
    """

    def __init__(
        self,
        file_path: Path | None = None,
        indent_on_save: int = 0,
        schema_url: str = "https://esi.evetech.net/meta/openapi.json",
    ) -> None:
        """Initialize SchemaStore, loading from file or downloading schema.

        Args:
            file_path (Path | None): Path to schema file, or None to download.
            schema_url (str): URL to download schema from.

        Raises:
            ValueError: If file_path is invalid or schema is invalid.
        """
        self._file_path = file_path
        self._schema_url = schema_url
        self._store_data: SchemaStoreData | None = None
        self._indent_on_save = indent_on_save

        if self._file_path is None:
            self._update_store()
        else:
            self._store_data = self._load_store_data()

    def update(self, save_to_file: bool = True) -> None:
        """Download schema and update the store, optionally saving to file.

        Args:
            save_to_file (bool): Whether to save schema to file after update.

        Raises:
            ValueError: If schema download fails.
        """
        self._update_store()
        if save_to_file:
            self._save_store_data()

    def _load_store_data(self) -> SchemaStoreData:
        """Load store data from file and validate its contents.

        Returns:
            SchemaStoreData: Loaded schema data and metadata.

        Raises:
            ValueError: If file is missing, invalid, or schema is invalid.
        """
        if self._file_path is None:
            raise ValueError("SchemaStore file_path is not set.")
        if not self._file_path.is_file():
            raise ValueError(f"SchemaStore file not found at: {self._file_path}")
        try:
            result = SchemaStoreData.model_validate_json(self._file_path.read_text())
            if "openapi" not in result.schema_:
                raise ValueError("Invalid ESI schema: 'openapi' key not found.")
        except Exception as e:
            raise ValueError(f"Failed to load ESI schema: {e}") from e
        return result

    def _save_store_data(self) -> None:
        """Save the store data to file.

        Raises:
            ValueError: If schema is not loaded or file path is not set.
        """
        if self._store_data is None:
            raise ValueError("ESI schema is not loaded. Nothing to save.")
        if self._file_path is None:
            raise ValueError("SchemaStore file_path is not set.")
        self._file_path.write_text(
            self._store_data.model_dump_json(indent=self._indent_on_save)
        )

    def _download_schema(self, url: str) -> dict[str, Any]:
        """Download a fresh copy of the ESI openapi schema.

        Args:
            url (str): URL to download schema from.

        Returns:
            dict[str, Any]: The downloaded schema as a dictionary.

        Raises:
            ValueError: If schema is invalid or missing 'openapi' key.
        """
        text = download_text(url)
        schema = json.loads(text)
        if "openapi" not in schema:
            raise ValueError("Invalid ESI schema: 'openapi' key not found.")
        return schema

    def _update_store(self) -> None:
        """Download the ESI OpenAPI schema and update the store.

        Raises:
            Exception: If schema download fails.
        """
        try:
            schema = self._download_schema(self._schema_url)
        except Exception as e:
            logger.error(f"Failed to update schema: {e}")
            raise e
        self._store_data = SchemaStoreData(
            id_=uuid4(), download_date=now_utc().isoformat(), schema_=schema
        )

    @property
    def esi_schema(self) -> dict[str, Any]:
        """Return the loaded ESI schema as a dictionary.

        Returns:
            dict[str, Any]: The ESI OpenAPI schema.

        Raises:
            ValueError: If schema is not loaded.
        """
        if self._store_data is None:
            raise ValueError("ESI schema is not loaded.")
        return self._store_data.schema_

    @property
    def schema_id(self) -> UUID:
        """Return the UUID of the loaded ESI schema.

        Returns:
            UUID: The unique identifier for the schema.

        Raises:
            ValueError: If schema is not loaded.
        """
        if self._store_data is None:
            raise ValueError("ESI schema is not loaded.")
        return self._store_data.id_

    @property
    def download_date(self) -> str:
        """Return the download date of the loaded ESI schema.

        Returns:
            str: The ISO 8601 UTC download datetime.

        Raises:
            ValueError: If schema is not loaded.
        """
        if self._store_data is None:
            raise ValueError("ESI schema is not loaded.")
        return self._store_data.download_date
