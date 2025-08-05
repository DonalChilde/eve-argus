"""ESI return data models."""

from typing import Any
from uuid import UUID

from pydantic import BaseModel


class EsiRequest(BaseModel):
    """Base class for ESI requests."""

    request_id: UUID
    op_id: str
    arguments: dict[str, Any] = {}
    parent: UUID | None = None
    """The parent request ID, if this is a sub-request."""


class EsiResponse(BaseModel):
    """Base class for ESI responses."""

    status_code: int = 0
    headers: dict[str, Any] = {}
    data: Any = None


class EsiAction(BaseModel):
    """Collection class to organize a single request and its response."""

    request: EsiRequest
    response: EsiResponse | None = None
    """The response to the request, if available."""
    pages: list["EsiAction"] = []
    """"A list of pages of data for the parent request."""


class DebugEsiAction(BaseModel):
    """A version of EsiAction without the subactions for debugging purposes."""

    request: EsiRequest
    response: EsiResponse | None = None
    """The response to the request, if available."""
