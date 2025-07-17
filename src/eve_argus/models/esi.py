"""ESI return data models."""

from dataclasses import dataclass, field
from typing import Any, TypedDict


@dataclass(slots=True)
class EsiRequest:
    """Base class for ESI requests."""

    op_id: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EsiResponse:
    """Base class for ESI responses."""

    headers: dict[str, Any] = field(default_factory=dict)
    data: Any = None
