"""API for retrieving public data from Eve ESI.

All code for woring with EsiResponse and EsiRequest models should live here.
"""

import json
import logging
from collections.abc import Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any
from uuid import uuid4

import preston

from eve_argus.data_import import esi_to_argus as DI
from eve_argus.models import argus as EAM
from eve_argus.models.esi import EsiRequest, EsiResponse
from eve_argus.snippets.file.datetime_filename import file_safe_datetime_string

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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
    response = EsiResponse(headers=dict(preston_client.stored_headers[0]), data=data)

    logger.info(
        f"ESI operation {esi_request.op_id} completed in {perf_counter() - start:.6f} seconds"
    )
    if debug_save:
        if debug_path is None:
            raise ValueError("debug_path must be provided when debug_save is True")
        _debug_save_esi_data(esi_request, response, debug_path)
    return response


def _debug_save_esi_data(
    esi_request: EsiRequest,
    esi_response: EsiResponse | Sequence[EsiResponse],
    debug_path: Path,
) -> None:
    """Save ESI request and response data for debugging."""
    debug_save_start = perf_counter()
    debug_path.mkdir(parents=True, exist_ok=True)
    file_name = (
        f"{file_safe_datetime_string(datetime.now(UTC))}_{esi_request.op_id}.json"
    )
    file_path = debug_path / file_name
    logger.info(f"Saving debug data to {file_path}")
    with open(file_path, "w", encoding="utf-8") as file_out:
        if isinstance(esi_response, Sequence):
            # If response is a sequence, convert each item to a dict
            file_data = {
                "request": asdict(esi_request),
                "response": [asdict(item) for item in esi_response],
            }
        elif isinstance(esi_response, EsiResponse):
            # Otherwise, convert the single response to a dict
            file_data = {
                "request": asdict(esi_request),
                "response": asdict(esi_response),
            }
        else:
            raise TypeError("esi_response must be EsiResponse or Sequence[EsiResponse]")
        json.dump(file_data, file_out, indent=2)
    logger.info(
        f"Debug data saved to {file_path} in {perf_counter() - debug_save_start:.6f} seconds."
    )


def _get_paged_esi_data(
    preston_client: preston.Preston,
    esi_request: EsiRequest,
    debug_save: bool = False,
    debug_path: Path | None = None,
) -> Sequence[EsiResponse]:
    """Helper function to get paged data from ESI."""
    start = perf_counter()
    logger.info(
        f"Requesting paged ESI operation {esi_request.op_id} with arguments {esi_request.arguments}"
    )

    paged_data: Sequence[EsiResponse] = []
    first_page = _get_esi_data(preston_client, esi_request)
    paged_data.append(first_page)
    # TODO check to see if there is a page header if only one page available
    # TODO consider an error if 'X-Pages' key not found when expected.
    page_count = int(first_page.headers.get("X-Pages", 1))
    logger.info(f"Retrieved page 1 of {page_count} for operation {esi_request.op_id}")
    for page in range(2, page_count + 1):
        esi_request.arguments["page"] = str(page)
        page_data = _get_esi_data(preston_client, esi_request)
        paged_data.append(page_data)
        logger.info(
            f"Retrieved page {page} of {page_count} for operation {esi_request.op_id}"
        )
    logger.info(
        f"Total pages retrieved for operation {esi_request.op_id}: {len(paged_data)} in {perf_counter() - start:.6f} seconds."
    )
    if debug_save:
        if debug_path is None:
            raise ValueError("debug_path must be provided when debug_save is True")
        _debug_save_esi_data(esi_request, paged_data, debug_path)
    return paged_data


class EsiPublic:
    def __init__(
        self,
        user_agent: str = "Eve Argus testing",
        debug: bool = False,
        debug_path: Path | None = None,
        preston_client: preston.Preston | None = None,
    ) -> None:
        """Initialize the EsiPublic client.

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
        self.preston = (
            preston_client if preston_client else preston.Preston(user_agent=user_agent)
        )
        self.debug = debug
        self.debug_path = debug_path
        start = perf_counter()
        # TODO trap server down error.
        # Do this to trigger download of swagger.json
        status = self.preston.get_op("get_status")
        logger.info(
            f"Initialized EsiPublic client in {perf_counter() - start:.6f} seconds. server status: {status!r}"
        )

    def get_market_history(self, region_id: int, type_id: int) -> EAM.MarketHistory:
        """Get market history for a specific region and type."""
        request = EsiRequest(
            op_id="get_markets_region_id_history",
            arguments={
                "region_id": str(region_id),
                "type_id": str(type_id),
            },
        )
        response = _get_esi_data(
            self.preston, request, debug_save=self.debug, debug_path=self.debug_path
        )
        result = DI.market_history(
            region_id=region_id, type_id=type_id, data=response.data
        )
        logger.info(
            f"Retrieved {len(result.data)} market history records for {request!r}."
        )
        return result

    def get_market_prices_universe(self) -> EAM.UniverseMarketPrices:
        """Get market prices for the entire universe."""
        request = EsiRequest(op_id="get_markets_prices")
        response = _get_esi_data(
            self.preston, request, debug_save=self.debug, debug_path=self.debug_path
        )
        data = DI.market_prices_universe(response.data)
        logger.info(f"Retrieved {len(data)} market prices for {request!r}.")
        result = EAM.UniverseMarketPrices(
            price_profile_id=uuid4(),
            date=datetime.now(UTC).isoformat(),
            data={item.type_id: item for item in data},
        )
        return result

    def get_region_market_types(self, region_id: int) -> Sequence[int]:
        """Get type ids with active market orders for a specific region."""
        request = EsiRequest(
            op_id="get_markets_region_id_types", arguments={"region_id": str(region_id)}
        )
        response = _get_paged_esi_data(
            self.preston, request, debug_save=self.debug, debug_path=self.debug_path
        )
        paged_data: Sequence[Sequence[int]] = [x.data for x in response]
        result = DI.region_market_types_from_esi(paged_data)
        logger.info(f"Retrieved {len(result)} market types for {request!r}.")
        return result

    def get_market_orders_by_region(
        self, region_id: int, order_type: str = "all"
    ) -> EAM.RegionalMarketOrders:
        """Get market orders for a specific region."""
        request = EsiRequest(
            op_id="get_markets_region_id_orders",
            arguments={"region_id": str(region_id), "order_type": order_type},
        )
        response = _get_paged_esi_data(
            self.preston, request, debug_save=self.debug, debug_path=self.debug_path
        )
        paged_data: Sequence[Sequence[dict[str, Any]]] = [x.data for x in response]
        result = DI.region_market_orders_from_esi(region_id, paged_data)
        logger.info(
            f"Retrieved {sum(len(page) for page in paged_data)} for {request!r}."
        )
        return result

    def get_market_orders_by_region_and_type(
        self, region_id: int, type_id: int, order_type: str = "all"
    ) -> EAM.MarketOrders:
        """Get market orders for a specific type in a region."""
        request = EsiRequest(
            op_id="get_markets_region_id_orders",
            arguments={
                "region_id": str(region_id),
                "type_id": str(type_id),
                "order_type": order_type,
            },
        )
        response = _get_paged_esi_data(
            self.preston, request, debug_save=self.debug, debug_path=self.debug_path
        )
        paged_data: Sequence[Sequence[dict[str, Any]]] = [x.data for x in response]
        result = DI.region_and_type_market_orders_from_esi(
            region_id, type_id, paged_data
        )
        logger.info(
            f"Retrieved {sum(len(page) for page in paged_data)} orders for {request!r}."
        )
        return result

    def get_system_cost_indices(self) -> EAM.SystemCostIndices:
        """Get system cost indices."""
        request = EsiRequest(op_id="get_industry_systems")
        response = _get_esi_data(
            self.preston, request, debug_save=self.debug, debug_path=self.debug_path
        )
        paged_data: Sequence[Sequence[dict[str, Any]]] = [x.data for x in response.data]
        result = DI.system_cost_indices_from_esi(paged_data)
        logger.info(
            f"Retrieved {len(result.data)} system cost indices for {request!r}."
        )
        return result
