"""ESI return data models."""

from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class EsiCacheMetadata(BaseModel):
    """Represents a cache metadata for ESI GET requests/responses."""

    cache_key: UUID
    """The cache key UUID, built from the get request url."""
    expires: str
    """The expiration time for the cache key in ISO 8601 format."""
    etag: str
    """The ETag for the cached response."""
    last_modified: str
    """The last modified time for the cached response in ISO 8601 format."""
    last_checked: str
    """The last time this ESI route was checked in ISO 8601 format."""


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


class EsiResponse(BaseModel):
    """Base class for ESI responses.

    This class is suitable for caching and managing ESI API responses.
    The text field is a list to support paged requests.
    """

    request_url: str
    cache_key: UUID | None
    """The cache key for the GET request/response, if available."""
    headers: tuple[tuple[str, str | None], ...] = ()
    text: list[str] = []
    """The response body as a list of strings to support paged requests."""


class EsiCachedResponse(BaseModel):
    """Represents a cached ESI response."""

    cache_key: UUID
    metadata: EsiCacheMetadata
    response: EsiResponse


class EsiCache(BaseModel):
    data: dict[UUID, EsiCachedResponse] = {}


class ResponseDataSource(StrEnum):
    """Represents the source of the ESI response data."""

    CACHE = "esi_cache"
    """The response was served from the esi client cache."""
    API = "esi_api"
    """The response was fetched from the ESI API."""
    EXTERNAL = "external"
    """Valid response data exists in an external source. This happens when a valid `etag` or
    `expires` is passed in from outside the esi client."""


class CacheMetadataSource(StrEnum):
    """Represents the source of the ESI cache metadata."""

    API = "esi_api"
    """The cache metadata was fetched from the ESI API."""
    EXTERNAL = "external"
    """The cache metadata was provided from an external source."""
    CACHE = "esi_cache"
    """The cache metadata was served from the esi client cache."""


class EsiAction(BaseModel):
    """Collection class to organize a single request and its response."""

    request: EsiRequest
    response: EsiResponse | None = None
    """The response to the request, if available."""
    cache_metadata: EsiCacheMetadata | None = None
    """The cache key for the GET request/response, if available."""
    metadata_source: CacheMetadataSource | None = None
    response_source: ResponseDataSource | None = None
    """The source of the ESI response data."""
