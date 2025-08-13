from collections.abc import Mapping
from typing import Protocol


class EveOpenApiProtocol(Protocol):
    def get_url(
        self,
        base_url: str,
        op_id: str,
        path_params: Mapping[str, str | int | float],
        query_params: Mapping[str, str | int | float],
        include_query: bool = False,
    ) -> str:
        """Build the URL for the given operation ID."""
        ...

    def validate_operation(
        self,
        op_id: str,
        path_params: Mapping[str, str | int | float],
        query_params: Mapping[str, str | int | float],
    ) -> bool:
        """Validate the operation parameters."""
        ...
