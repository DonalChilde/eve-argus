"""API for retrieving public data from Eve ESI.

All code for woring with EsiResponse and EsiRequest models should live here.
"""

import logging
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import preston

from eve_argus.esi_client.esi_client_protocol import EsiClientProtocol
from eve_argus.models.esi import DebugEsiAction, EsiAction, EsiRequest, EsiResponse
from eve_argus.snippets.file.datetime_filename import file_safe_datetime_string

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# TODO split this class to EsiRequests for top level object, and ArgusPreston for specific implementation.
## Do this to support easier later change to httpx or other client.
# TODO autodetect paged data from swagger.json.


def _get_esi_data(
    preston_client: preston.Preston,
    esi_request: EsiRequest,
    debug_save: bool = False,
    debug_path: Path | None = None,
) -> EsiResponse:
    """Helper function to get data from ESI using a Preston client."""
    start = perf_counter()
    logger.info(
        f"Requesting ESI operation {esi_request.op_id} with arguments {esi_request.arguments}"
    )
    data = preston_client.get_op(esi_request.op_id, **esi_request.arguments)
    # Enforce lowercase for header field names
    # TODO check to see if cached response returns correct headers. Bet it doesnt.
    headers = {
        key.lower(): value for key, value in preston_client.stored_headers[0].items()
    }
    response = EsiResponse(headers=headers, data=data)

    logger.info(
        f"ESI operation {esi_request.op_id} completed in {perf_counter() - start:.6f} seconds"
    )
    if debug_save:
        if debug_path is None:
            raise ValueError("debug_path must be provided when debug_save is True")
        _debug_save_esi_data(esi_request, response, debug_path)
    return response


def _get_esi_data_bulk(
    preston_client: preston.Preston,
    esi_actions: Sequence[EsiAction],
    debug_save: bool = False,
    debug_path: Path | None = None,
) -> None:
    """Make multiple requests to ESI to fill response value for EsiActions."""
    # TODO consider multithreaded requests to speed up bulk requests.
    for esi_action in esi_actions:
        response = _get_esi_data(
            preston_client, esi_action.request, debug_save, debug_path
        )
        esi_action.response = response

    return None


def _debug_save_esi_data(
    esi_request: EsiRequest,
    esi_response: EsiResponse,
    debug_path: Path,
) -> None:
    """Save ESI request and response data for debugging."""
    if not debug_path:
        raise ValueError("debug_path must be provided to save debug data")
    debug_save_start = perf_counter()
    debug_path.mkdir(parents=True, exist_ok=True)
    file_name = (
        f"{file_safe_datetime_string(datetime.now(UTC))}_{esi_request.op_id}.json"
    )
    file_path = debug_path / file_name
    logger.info(f"Saving debug data to {file_path}")
    with open(file_path, "w", encoding="utf-8") as file_out:
        debug_action = DebugEsiAction(request=esi_request, response=esi_response)
        file_out.write(debug_action.model_dump_json(indent=2))
    logger.info(
        f"Debug data saved to {file_path} in {perf_counter() - debug_save_start:.6f} seconds."
    )


def _build_paged_requests(parent_action: EsiAction) -> None:
    """Build a list of paged ESI requests from a parent action."""
    if parent_action.response is None:
        raise ValueError("Parent action must have a response to build paged requests.")
    page_count = int(parent_action.response.headers.get("x-pages", 1))
    for page in range(2, page_count + 1):
        new_request = EsiRequest(
            request_id=uuid4(),
            op_id=parent_action.request.op_id,
            arguments={**parent_action.request.arguments, "page": str(page)},
            parent_id=parent_action.request.request_id,
        )
        action = EsiAction(request=new_request)
        parent_action.pages.append(action)
    return None


class ArgusPreston(EsiClientProtocol):
    """Class to handle ESI requests and responses using Preston client."""

    def __init__(
        self,
        user_agent: str = "Eve Argus testing",
        debug: bool = False,
        debug_path: Path | None = None,
        preston_client: preston.Preston | None = None,
    ) -> None:
        """Initialize the ArgusPreston client.

        The preston client downloads the swagger.json file on first request, and stores it
        in client.spec, so this constructor will take some time on first use. A preconfigured
        Preston client can be passed in to avoid this delay. To pre-configure another
        Preston client, make a new client or copy a current client, then set the
        new_client.spec = old_client.spec before first use of new_client.

        Args:
            user_agent (str): User agent for the ESI requests.
            debug (bool): Whether to enable debug mode.
            debug_path (Path | None): Path to save debug data.
            preston_client (preston.Preston | None): Optional existing Preston client.
        """
        self.preston_client = (
            preston_client if preston_client else preston.Preston(user_agent=user_agent)
        )
        self.debug = debug
        self.debug_path = debug_path
        start = perf_counter()
        # TODO trap server down error.
        # Do this to trigger download of swagger.json
        status = self.preston_client.get_op("get_status")
        logger.info(
            f"Initialized EsiPublic client in {perf_counter() - start:.6f} seconds. server status: {status!r}"
        )

    def get_esi_data(
        self,
        action: EsiAction,
    ) -> None:
        """Get data from ESI.

        Paged data is detected and downloaded automatically.
        The paged data is stored in the action.pages list.
        If the response has an 'x-pages' header, it is assumed to be paged data.
        """
        response = _get_esi_data(
            self.preston_client, action.request, self.debug, self.debug_path
        )
        action.response = response
        if "x-pages" in response.headers:
            _build_paged_requests(action)
            _get_esi_data_bulk(
                self.preston_client, action.pages, self.debug, self.debug_path
            )
        return None

    def get_esi_data_batch(self, actions: Sequence[EsiAction]) -> None:
        """Get operation data from ESI for a sequence of requests."""
        _get_esi_data_bulk(self.preston_client, actions, self.debug, self.debug_path)
        return None
