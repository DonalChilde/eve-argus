"""ESI return data models."""

from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel


# TODO change these to BaseModel, and use DebugRequest class for serialization.
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


class DebugRequest(BaseModel):
    """A request and response for debugging and serializing purposes."""

    request: EsiRequest
    """The ESI request being made."""
    response: EsiResponse
    """The ESI response received."""
