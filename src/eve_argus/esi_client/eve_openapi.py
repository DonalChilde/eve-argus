""""""

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Literal


class EveOpenApi:
    def __init__(self, spec_path: Path) -> None:
        self.spec_path = spec_path
        self.spec: dict[str, Any] = self._load_spec()

    def _load_spec(self) -> dict[str, Any]:
        """Load the OpenAPI specification from the specified file."""
        with open(self.spec_path, encoding="utf-8") as file:
            return json.load(file)

    def _collect_path_params(
        self, op_id: str, operation: Literal["get", "put", "post", "delete"]
    ) -> dict[str, dict[str, Any]]:
        """Collect the path parameters for the given operation ID from the schema.

        Args:
            op_id (str): The operation ID.
            operation (Literal["get", "put", "post", "delete"]): The HTTP operation type.

        Returns:
            dict[str, str]: A dictionary of path parameters.
        """
        # Get the path parameters from the spec
        # path parameters must have unique names, so we use a dict to enforce this.
        op_path_params = self.spec.get("paths", {}).get(op_id, {}).get("parameters", [])
        return {
            param["name"]: param
            for param in op_path_params
            if param.get("in") == "path"
        }

    def _check_path_params(
        self,
        op_id: str,
        operation: Literal["get", "put", "post", "delete"],
        path_params: dict[str, str],
    ) -> bool:
        """Check if the required path parameters are present for the given operation ID.

        Args:
            op_id (str): The operation ID.
            operation (Literal["get", "put", "post", "delete"]): The HTTP operation type.
            path_params (dict[str, str]): A dictionary of path parameters.

        Returns:
            bool: True if all required path parameters are present, False otherwise.
        """
        # Get the list of required path parameters from the spec
        required_params = self._collect_path_params(op_id, operation)

        # Check no extra path parameters are provided in path_params
        if not all(path_param in required_params for path_param in path_params):
            raise ValueError(
                f"Unrecognized path parameters given.:{path_params=}, {required_params=}"
            )

        # Check if all required parameters are present in the provided path_params
        if not all(required_param in path_params for required_param in required_params):
            raise ValueError(
                f"Missing required path parameters: {path_params=}, {required_params=}"
            )
        return True

    def _collect_path(self, op_id: str) -> str:
        """Get the path for the given operation ID.

        Args:
            op_id (str): The operation ID.

        Returns:
            str: The path for the operation.
        """
        path = self.spec.get("paths", {}).get(op_id, {}).get("path", "")
        if not path:
            raise ValueError(f"Path not found for operation ID: {op_id}")
        return path

    def _collect_query_params(
        self, op_id: str, operation: Literal["get", "put", "post", "delete"]
    ) -> dict[str, dict[str, Any]]:
        """Collect the query parameters for the given operation ID from the schema.

        Args:
            op_id (str): The operation ID.
            operation (Literal["get", "put", "post", "delete"]): The HTTP operation type.

        Returns:
            dict[str, str]: A dictionary of query parameters.
        """
        # Get the query parameters from the spec
        # Query strings do not have to have unique names, but Eve esi uses unique names
        # for query parameters, and they are all defined in the operation path.
        op_query_params = (
            self.spec.get("paths", {}).get(op_id, {}).get("parameters", [])
        )
        return {
            param["name"]: param
            for param in op_query_params
            if param.get("in") == "query"
        }

    def _check_query(
        self,
        op_id: str,
        operation: Literal["get", "put", "post", "delete"],
        query_params: dict[str, str],
    ) -> bool:
        """Check if the required query parameters are present for the given operation ID.

        Args:
            op_id (str): The operation ID.
            query_params (dict[str, str]): A dictionary of query parameters.
            operation (Literal["get", "put", "post", "delete"]): The HTTP operation type.

        Returns:
            bool: True if all required query parameters are present, False otherwise.
        """
        # Get the list of required query parameters from the spec
        possible_params = self._collect_query_params(op_id, operation)

        # Check no extra query parameters are provided in query_params
        if not all(query_param in possible_params for query_param in query_params):
            raise ValueError(
                f"Unrecognized query parameters given: {query_params=}, {possible_params=}"
            )

        # Check if all required parameters are present in the provided query_params
        for key, value in possible_params.items():
            if value.get("required", False):
                if key not in query_params:
                    raise ValueError(
                        f"Missing required query parameters: {query_params=}, {possible_params=}"
                    )
        return True

    def get_url(
        self,
        base_url: str,
        op_id: str,
        operation: Literal["get", "put", "post", "delete"],
        path_params: dict[str, str],
        query_params: dict[str, str],
    ) -> str:
        """Build a complete URL by combining the base URL, operation ID, path parameters, and query parameters.

        Args:
            base_url (str): The base URL.
            op_id (str): The operation ID (path component).
            operation (Literal["get", "put", "post", "delete"]): The HTTP operation type.
            path_params (dict[str, str]): A dictionary of path parameters to include in the URL.
            query_params (dict[str, str]): A dictionary of query parameters to include in the URL.

        Returns:
            str: The constructed URL.
        """
        self._check_path_params(op_id, operation, path_params)
        # Build the path by replacing placeholders with actual values
        path_template = self._collect_path(op_id)
        path = path_template.format(**path_params)

        resolved_url = f"{base_url.strip('/')}/{path.strip('/')}"

        # Construct the query string from the query parameters
        self._check_query(op_id, operation, query_params)
        query_string = "&".join(
            [f"{key}={value}" for key, value in query_params.items()]
        )

        # Combine the path and query string into the final URL
        return f"{resolved_url}?{query_string}" if query_string else resolved_url

    def _collect_submit_headers(
        self, op_id: str, operation: Literal["get", "put", "post", "delete"]
    ) -> dict[str, dict[str, Any]]:
        """Collect the headers for the given operation ID from the schema.

        Args:
            op_id (str): The operation ID.
            operation (Literal["get", "put", "post", "delete"]): The HTTP operation type.

        Returns:
            dict[str, dict[str, Any]]: A dictionary of headers.
        """
        return {
            header["name"]: header
            for header in self.spec.get("paths", {}).get(op_id, {}).get("headers", [])
        }

    def _collect_response_headers(
        self, op_id: str, operation: Literal["get", "put", "post", "delete"]
    ) -> dict[str, dict[str, Any]]:
        """Collect the response headers for the given operation ID from the schema.

        Args:
            op_id (str): The operation ID.
            operation (Literal["get", "put", "post", "delete"]): The HTTP operation type.

        Returns:
            dict[str, dict[str, Any]]: A dictionary of response headers.
        """
        # FIXME resolve full header infomation, both common and specific.
        return {
            header["name"]: header
            for header in self.spec.get("paths", {})
            .get(op_id, {})
            .get("responses", {})
            .get("headers", {})
        }

    def _collect_operation_headers(
        self, op_id: str, operation: Literal["get", "put", "post", "delete"]
    ) -> dict[str, dict[str, Any]]:
        """Collect the headers for the given operation ID from the schema.

        Args:
            op_id (str): The operation ID.
            operation (Literal["get", "put", "post", "delete"]): The HTTP operation type.

        Returns:
            dict[str, dict[str, Any]]: A dictionary of headers.
        """
        # FIXME resolve full header infomation, both common and specific.
        return {
            header["name"]: header
            for header in self.spec.get("paths", {}).get(op_id, {}).get("headers", {})
        }
