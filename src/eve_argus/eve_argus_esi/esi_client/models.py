from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class EsiRequest(BaseModel):
    """Base class for ESI requests."""

    request_id: UUID
    op_id: str
    method: Literal["get", "post", "put", "delete"]
    path_params: dict[str, str | int | float] = {}
    url: str
    """The URL for the request, without query parameters."""
    query_params: dict[str, str | int | float] = {}
    paged: bool
    """Whether the request expects a paged response."""
    cache_key: UUID | None = None
    """The cache key UUID, built from the get request url, if cacheable."""
    headers: dict[str, str] = {}
    parent_id: UUID | None = None
    """The parent request ID, if this is a sub-request."""
    parent_last_modified: str | None = None
    """The parent request last modified timestamp, if this is a paged sub-request."""
    etag: str = ""
    """The ETag for the request, if checking a stale cache entry."""


# class PagedRequest(BaseModel):
#     """Base class for ESI paged requests."""

#     request_id: UUID
#     op_id: str
#     method: Literal["GET", "POST", "PUT", "DELETE"]
#     path_params: dict[str, str | int | float] = {}
#     url: str | None = None
#     """The URL for the request, without query parameters."""
#     query_params: dict[str, str | int | float] = {}
#     headers: dict[str, str | None] = {}
#     parent_id: UUID | None = None
#     """The parent request ID, if this is a sub-request."""
#     parent_last_modified: str | None = None
#     """The parent request last modified timestamp, if this is a paged sub-request."""
#     # A paged request who's last-modified header does not match the parent last-modified
#     # indicates that the data has changed since the parent request, the pages are no longer valid.


# class EsiPagedResponse(BaseModel):
#     real_url: str
#     headers: tuple[tuple[str, str | None], ...] = ()
#     status_code: int
#     status_reason: str
#     page: int
#     """The page number of the response."""
#     text: str
#     """The response body as a list of strings to support paged requests."""
#     completed_on: str
#     """The datetime the response completed, in UTC, in ISO Format."""
#     last_modified: str | None = None
#     """The last-modified header of the response, if available."""


class EsiResponse(BaseModel):
    """Base class for ESI responses.

    This class is suitable for caching and managing ESI API responses.
    """

    real_url: str
    cache_key: UUID | None
    """The cache key for the GET request/response, if available."""
    headers: tuple[tuple[str, str | None], ...] = ()
    text: str
    status_code: int
    status_reason: str
    completed_on: str
    """The datetime the response completed, in UTC, in ISO Format."""
    paged_responses: list[str] = []
    """The paged responses, if any."""


class EsiAction(BaseModel):
    """Collection class to organize a single request and its response."""

    request: EsiRequest
    response: EsiResponse | None = None
    """The response to the request, if available."""


# class PagedAction(BaseModel):
#     """Collection class to organize a paged request and its responses."""

#     request: PagedRequest
#     response: EsiPagedResponse | None = None
#     """The response to the request, if available."""
