"""The manifest model for eve-argus file data."""

from uuid import UUID

from pydantic import BaseModel


class FileManifest(BaseModel):
    """A manifest for a file in the eve-argus data system."""

    uuid_key: UUID
    """Unique identifier for the file."""
    file_name_keys: dict[str, str] = {}
    created_at: str
    """UTC Datetime when the file was created in ISO format."""
    attributes: dict[str, str] = {}


class StaticDataFiles(BaseModel):
    """A collection of static data files in the eve-argus data system."""

    date_generated: str
    """UTC Datetime when the static data files were generated in ISO format."""
    sde_download_date: str = ""
    """SDE download date if known, otherwise empty string."""
    sde_version: str = ""
    """SDE version if known, otherwise empty string."""

    types: FileManifest | None = None
    blueprints: FileManifest | None = None
    market_groups: FileManifest | None = None
    meta_groups: FileManifest | None = None
    groups: FileManifest | None = None
    categories: FileManifest | None = None


class ArgusFilesManifest(BaseModel):
    static_data: dict[UUID, FileManifest] = {}
