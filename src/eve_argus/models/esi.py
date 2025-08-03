"""ESI return data models."""

from typing import Any
from uuid import UUID

from pydantic import BaseModel


class EsiRequest(BaseModel):
    """Base class for ESI requests."""

    request_id: UUID
    op_id: str
    arguments: dict[str, Any] = {}


class EsiResponse(BaseModel):
    """Base class for ESI responses."""

    # TODO enforce lowercase for header field names
    headers: dict[str, Any] = {}
    data: Any = None


class EsiAction(BaseModel):
    """Collection class to organize a single request and its response."""

    request: EsiRequest
    response: EsiResponse
