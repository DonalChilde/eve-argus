from collections.abc import Mapping
from typing import Protocol, TypedDict


class SplitParameters(TypedDict):
    path: Mapping[str, str | int | float]
    query: Mapping[str, str | int | float]
    header: Mapping[str, str | int | float]


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

    def split_parameters(
        self,
        op_id: str,
        parameters: Mapping[str, str | int | float],
    ) -> SplitParameters:
        """Split the parameters into their respective categories."""
        ...

    def is_paged(self, op_id: str) -> bool:
        """Check if the operation is paged."""
        ...
