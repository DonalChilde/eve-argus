"""ESI return data models."""

from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel


class EsiRequest(BaseModel):
    """Base class for ESI requests."""

    request_id: UUID
    op_id: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    path_params: dict[str, str | int | float] = {}
    query_params: dict[str, str | int | float] = {}
    headers: dict[str, str | None] = {}
    parent_id: UUID | None = None
    """The parent request ID, if this is a sub-request."""
    # cache_key: UUID | None = None
    # """The cache key for the GET request/response, if available."""


class EsiResponse(BaseModel):
    """Base class for ESI responses.

    This class is suitable for caching and managing ESI API responses.
    The text field is a list to support paged requests.
    """

    request_id: UUID
    request_url: str
    source: Literal["esi_cache", "esi_api", "not_set"] = "not_set"
    cache_key: UUID | None
    """The cache key for the GET request/response, if available."""
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
