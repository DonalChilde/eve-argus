from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import UUID, uuid4


@dataclass(slots=True)
class HttpRequest:
    method: Literal["GET", "POST", "PUT", "DELETE"]
    url: str
    query_params: dict[str, str | int | float] = field(default_factory=dict)
    headers: list[tuple[str, str]] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)
    uuid: UUID = field(default_factory=uuid4)
    parent_uuid: UUID | None = None


@dataclass(slots=True)
class HttpResponse:
    request_id: UUID
    request_url: str
    cache_key: UUID | None
    """The cache key for the GET request/response, if available."""
    status_code: int
    status_reason: str | None
    headers: Sequence[tuple[str, str]]
    expires: str
    etag: str
    last_modified: str
    text: list[str] = []
    kwargs: dict[str, Any] = field(default_factory=dict)
    uuid: UUID = field(default_factory=uuid4)
    source: Literal["cache", "api", "not_set"] = "not_set"


@dataclass(slots=True)
class HttpAction:
    request: HttpRequest
    response: HttpResponse | None = None
