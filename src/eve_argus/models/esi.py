"""ESI return data models."""

from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel


class EsiRequest(BaseModel):
    """Base class for ESI requests."""

    request_id: UUID
    op_id: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    path_params: dict[str, str] = {}
    query_params: dict[str, str | int | float] = {}
    headers: dict[str, str | None] = {}
    parent: UUID | None = None
    """The parent request ID, if this is a sub-request."""
    cache_key: UUID | None
    """The cache key for the request/response, if available."""


class EsiResponse(BaseModel):
    """Base class for ESI responses.

    This class is suitable for caching and managing ESI API responses.
    The text field is a list to support paged requests.
    """

    request_id: UUID
    request_url: str
    source: Literal["cache", "api"] = "api"
    cache_key: UUID | None
    """The cache key for the request/response, if available."""
    text: list[str] = []
    """The response body as a list of strings."""
    expires: str
    etag: str
    last_modified: str


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
