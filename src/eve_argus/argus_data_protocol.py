from typing import Any, Protocol

from eve_argus.models import argus as EAM


class StoreDataProtocol(Protocol):
    """Protocol for data storage operations."""

    def type_infos(self, data_set: EAM.TypeInfos) -> None:
        """Store type information in the Argus data store."""
        ...

    def type_descriptions(self, data_set: EAM.TypeDescriptions) -> None:
        """Store type descriptions in the Argus data store."""
        ...


class RetrieveDataProtocol(Protocol):
    """Protocol for data retrieval operations."""

    def type_infos(self) -> EAM.TypeInfos | None:
        """Retrieve type information from the Argus data store."""
        ...

    def type_descriptions(self) -> EAM.TypeDescriptions | None:
        """Retrieve type descriptions from the Argus data store."""
        ...


class DeleteDataProtocol(Protocol):
    """Protocol for data deletion operations."""

    def type_infos(self) -> None:
        """Delete type information from the Argus data store."""
        ...

    def type_descriptions(self) -> None:
        """Delete type descriptions from the Argus data store."""
        ...


class ArgusDataStoreProtocol(Protocol):
    """Protocol for Argus data storage operations."""

    def store(self) -> StoreDataProtocol:
        """Store data in the Argus data store."""
        ...

    def retrieve(self) -> RetrieveDataProtocol:
        """Retrieve data from the Argus data store."""
        ...

    def delete(self) -> DeleteDataProtocol:
        """Delete data from the Argus data store."""
        ...

    def status(self) -> Any:
        """Get the status of the datasets in the data store, eg. presence, expiration, effective date."""
        ...

    def manifest(self) -> Any:
        """Get the manifest of the datasets in the data store, eg. dataset names, versions, etc."""
        ...


# make a file system version, and a database version of the ArgusDataStoreProtocol
