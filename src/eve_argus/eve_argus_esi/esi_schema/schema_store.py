"""SchemaStore supports managing the ESI openapi schema.

The schema is loaded from a file if it exists, and can be updated by downloading a
fresh copy from the ESI API.
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


class EsiSchema(BaseModel):
    id_: UUID
    """The unique identifier of the schema."""
    download_date: str
    """The download date (UTC) of the schema in ISO 8601 format."""
    schema_: dict[str, Any]
    """The ESI OpenAPI schema as a dictionary."""


# TODO custom exceptions


class SchemaStore:
    def __init__(
        self,
        file_path: Path,
        schema_url: str = "https://esi.evetech.net/meta/openapi.json",
    ) -> None:
        """Manages the ESI OpenAPI schema.

        Can be loaded from a file or downloaded from the ESI API.
        """
        self.file_path = file_path
        self.schema_url = schema_url
        self._esi_schema = None

    def __enter__(self):
        """Enter the runtime context related to this object.

        Loads the ESI schema from file if available.
        """
        self._esi_schema = self._load_schema()
        if self._esi_schema is None:
            schema = self._download_schema(self.schema_url)
            self._esi_schema = EsiSchema(
                id_=uuid4(), download_date=now_utc().isoformat(), schema_=schema
            )
            self._save_schema()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        """Exit the runtime context and save the ESI schema to file."""
        self._save_schema()

    def _load_schema(self) -> EsiSchema | None:
        if not self.file_path.is_file():
            return None
        result = EsiSchema.model_validate_json(self.file_path.read_text())
        return result

    def _save_schema(self) -> None:
        if self._esi_schema is None:
            return
        self.file_path.write_text(self._esi_schema.model_dump_json())

    def _download_schema(self, url: str) -> dict[str, Any]:
        """Download a fresh copy of the ESI openapi schema."""
        text = download_text(url)
        schema = json.loads(text)
        return schema

    def update_schema(self) -> None:
        """Download and store a fresh copy of the ESI openapi schema."""
        try:
            schema = self._download_schema(self.schema_url)
        except Exception as e:
            logger.error(f"Failed to update schema: {e}")
            raise e
        self._esi_schema = EsiSchema(
            id_=uuid4(), download_date=now_utc().isoformat(), schema_=schema
        )

    @property
    def esi_schema(self) -> dict[str, Any]:
        """Return the loaded ESI schema as a dictionary."""
        if self._esi_schema is None:
            raise ValueError("ESI schema is not loaded.")
        return self._esi_schema.schema_

    @property
    def schema_id(self) -> UUID:
        """Return the UUID of the loaded ESI schema."""
        if self._esi_schema is None:
            raise ValueError("ESI schema is not loaded.")
        return self._esi_schema.id_

    @property
    def download_date(self) -> str:
        """Return the download date of the loaded ESI schema."""
        if self._esi_schema is None:
            raise ValueError("ESI schema is not loaded.")
        return self._esi_schema.download_date
