"""Code to interact with the Eve Esi openapi spec."""

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any, TypedDict

from eve_argus.esi_schema.eve_openapi_protocol import EveOpenApiProtocol

# FIXME decide on validation signalling. right now the functions return a bool, and throw an exception.
# TODO output a table of operation_ids,paths, descriptions, and valid inputs.


class ByOpId(TypedDict):
    operationId: str
    method: str
    path: str
    operation: dict[str, Any]

    # def validate_operation_headers(
    #     self, op_id: str, headers: dict[str, str | None]
    # ) -> bool:
    #     """Validate the operation headers."""
    #     ...


class EveOpenApi(EveOpenApiProtocol):
    def __init__(
        self, spec_path: Path | None = None, spec: dict[str, Any] | None = None
    ) -> None:
        """Initialize the EveOpenApi client."""
        if spec_path is None and spec is None:
            raise ValueError("Either spec_path or spec must be provided.")
        self.spec_path = spec_path
        self.spec: dict[str, Any] = spec or self._load_spec()
        self.by_op_id: dict[str, ByOpId] = self._index_by_op_id()

    def _resolve_ref(self, reference: str) -> dict[str, Any]:
        """Resolve a JSON reference (RFC 6901) to its definition in the spec."""
        if reference.startswith("#/"):
            # Resolve internal reference
            parts = reference[2:].split("/")
            return self._resolve_internal_ref(parts)
        return {}

    def _resolve_internal_ref(self, parts: list[str]) -> dict[str, Any]:
        """Resolve an internal JSON reference given as a list of path parts."""
        obj = self.spec
        for part in parts:
            if isinstance(obj, dict):
                obj = obj.get(part)
            else:
                return {}
        return obj if isinstance(obj, dict) else {}

    def _common_response_headers(self) -> dict[str, dict[str, Any]]:
        response_headers = {}
        for header in self.spec.get("components", {}).get("headers", {}).values():
            response_headers[header["name"]] = header
        return response_headers

    def _common_request_headers(self) -> dict[str, dict[str, Any]]:
        request_headers = {}
        for header in self.spec.get("components", {}).get("headers", {}).values():
            if header.get("in") == "header":
                request_headers[header["name"]] = header
        return request_headers

    def _operation_specific_response_parameters(
        self, operation_id: str
    ) -> dict[str, dict[str, Any]]:
        """Get the response headers specific to the given operation ID."""
        operation = self.by_op_id.get(operation_id, {})
        response_headers: dict[str, dict[str, Any]] = {}
        for key, value in (
            operation.get("operation", {})
            .get("responses", {})
            .get("200", {})
            .get("headers", {})
            .items()
        ):
            if "$ref" in value:
                response_headers[key] = self._resolve_ref(value["$ref"])
            else:
                response_headers[key] = value
        return response_headers

    def _operation_specific_request_parameters(
        self, operation_id: str
    ) -> dict[str, dict[str, Any]]:
        """Get the request parameters specific to the given operation ID."""
        operation = self.by_op_id.get(operation_id, {})
        request_parameters: dict[str, dict[str, Any]] = {}
        for value in operation.get("operation", {}).get("parameters", []):
            if "$ref" in value:
                value = self._resolve_ref(value["$ref"])
                request_parameters[value["name"]] = value
            else:
                request_parameters[value["name"]] = value
        return request_parameters

    def _index_by_op_id(self) -> dict[str, ByOpId]:
        """Index the operations by their ID."""
        by_op_id: dict[str, ByOpId] = {}
        for path, methods in self.spec.get("paths", {}).items():
            for method, operation in methods.items():
                op_id = operation.get("operationId")
                if op_id:
                    by_op_id[op_id] = ByOpId(
                        operationId=op_id,
                        method=method.upper(),
                        path=path,
                        operation=operation,
                    )
        return by_op_id

    def _load_spec(self) -> dict[str, Any]:
        """Load the OpenAPI specification from the specified file."""
        if self.spec_path is None or not self.spec_path.exists():
            raise ValueError(f"Spec path is invalid: {self.spec_path}")
        with open(self.spec_path, encoding="utf-8") as file:
            return json.load(file)

    def _collect_path_params(self, op_id: str) -> dict[str, dict[str, Any]]:
        """Collect the path parameters for the given operation ID from the schema.

        Args:
            op_id (str): The operation ID.

        Returns:
            dict[str, dict[str, Any]]: A dictionary of path parameter definitions keyed by
            parameter name.

        Example:
            For ``op_id='GetMarketsRegionIdHistory'`` (path ``/markets/{region_id}/history``)
            this function returns a mapping like:

                {
                    "region_id": {
                        "in": "path",
                        "name": "region_id",
                        "required": True,
                        "schema": {
                            "description": "Return statistics in this region",
                            "format": "int64",
                            "type": "integer"
                        }
                    }
                }
        """
        # Get the path parameters from the spec
        # path parameters must have unique names, so we use a dict to enforce this.
        op_parameters = self._operation_specific_request_parameters(operation_id=op_id)
        path_parameters = {}
        for key, param in op_parameters.items():
            if param.get("in") == "path":
                path_parameters[key] = param
        return path_parameters

    def _check_path_params(
        self,
        op_id: str,
        path_params: Mapping[str, str | int | float],
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
        required_params = self._collect_path_params(op_id=op_id)

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
        path = self.by_op_id.get(op_id, {}).get("path")
        if not path:
            raise ValueError(f"Path not found for operation ID: {op_id}")
        return path

    def _collect_query_params(self, op_id: str) -> dict[str, dict[str, Any]]:
        """Collect the query parameters for the given operation ID from the schema.

        Args:
            op_id (str): The operation ID.

        Returns:
            dict[str, dict[str, Any]]: A dictionary of query parameter definitions
            keyed by parameter name.

        Example:
            For ``op_id='GetMarketsRegionIdHistory'`` (path ``/markets/{region_id}/history``)
            this function returns a mapping like:

                {
                    "type_id": {
                        "in": "query",
                        "name": "type_id",
                        "required": True,
                        "schema": {
                            "description": "Return statistics for this type",
                            "format": "int64",
                            "type": "integer"
                        }
                    }
                }
        """
        # Get the query parameters from the spec
        # Query strings do not have to have unique names, but Eve esi uses unique names
        # for query parameters, and they are all defined in the operation path.
        operation_parameters = self._operation_specific_request_parameters(
            operation_id=op_id
        )
        query_params = {}
        for key, param in operation_parameters.items():
            if param.get("in") == "query":
                query_params[key] = param
        return query_params

    def _check_query(
        self,
        op_id: str,
        query_params: Mapping[str, str | int | float],
    ) -> bool:
        """Check if the required query parameters are present for the given operation ID.

        Args:
            op_id (str): The operation ID.
            query_params (dict[str, str]): A dictionary of query parameters.

        Returns:
            bool: True if all required query parameters are present, False otherwise.
        """
        # Get the list of required query parameters from the spec
        possible_params = self._collect_query_params(op_id=op_id)

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

    def validate_operation(
        self,
        op_id: str,
        path_params: Mapping[str, str | int | float],
        query_params: Mapping[str, str | int | float],
    ) -> bool:
        """Validate the operation parameters."""
        valid = all(
            (
                self._check_path_params(op_id=op_id, path_params=path_params),
                self._check_query(op_id=op_id, query_params=query_params),
            ),
        )
        return valid

    def get_url(
        self,
        base_url: str,
        op_id: str,
        path_params: Mapping[str, str | int | float],
        query_params: Mapping[str, str | int | float],
        include_query: bool = False,
    ) -> str:
        """Build a complete URL by combining the base URL, operation ID, path parameters, and query parameters.

        Args:
            base_url (str): The base URL.
            op_id (str): The operation ID (path component).
            operation (Literal["get", "put", "post", "delete"]): The HTTP operation type.
            path_params (dict[str, str]): A dictionary of path parameters to include in the URL.
            query_params (dict[str, str]): A dictionary of query parameters to include in the URL.
            include_query (bool): Whether to include the query parameters in the URL.

        Returns:
            str: The constructed URL.
        """
        self.validate_operation(
            op_id=op_id, path_params=path_params, query_params=query_params
        )
        # Build the path by replacing placeholders with actual values
        path_template = self._collect_path(op_id)
        path = path_template.format(**path_params)

        resolved_url = f"{base_url.strip('/')}/{path.strip('/')}"

        if include_query:
            # Construct the query string from the query parameters
            # Sort keys so URL is stable regardless of dict insertion order
            query_items = sorted(query_params.items(), key=lambda kv: kv[0])
            query_string = "&".join([f"{key}={value}" for key, value in query_items])
            # Combine the path and query string into the final URL
            return f"{resolved_url}?{query_string}" if query_string else resolved_url

        return resolved_url

    def _collect_request_headers(self, op_id: str) -> dict[str, dict[str, Any]]:
        """Collect the headers for the given operation ID from the schema.

        Args:
            op_id (str): The operation ID.

        Returns:
            dict[str, dict[str, Any]]: A dictionary of headers.
        """
        request_parameters = self._operation_specific_request_parameters(op_id)
        request_headers = {}
        for key, param in request_parameters.items():
            if param.get("in") == "header":
                request_headers[key] = param
        return request_headers

    def _collect_response_headers(self, op_id: str) -> dict[str, dict[str, Any]]:
        """Collect the possible response headers for the given operation ID from the schema.

        Includes headers in common, and those specific to the operation.

        Args:
            op_id (str): The operation ID.

        Returns:
            dict[str, dict[str, Any]]: A dictionary of response headers.
        """
        response_parameters = self._operation_specific_response_parameters(op_id)
        response_headers = {}
        for key, param in response_parameters.items():
            if param.get("in") == "header":
                response_headers[key] = param
        return response_headers
