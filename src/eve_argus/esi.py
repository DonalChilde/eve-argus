"""API for retrieving public data from Eve ESI."""

import logging
from collections.abc import Sequence
from time import perf_counter
from typing import Any
from itertools import chain

import preston

from eve_argus.models import argus as EAM
from eve_argus.util.esi import import_market_prices_universe

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class EsiPublic:
    def __init__(self, user_agent: str = "Eve Argus testing") -> None:
        self.preston = preston.Preston(user_agent=user_agent)

    def get_market_history(
        self, region_id: int, type_id: int
    ) -> Sequence[EAM.MarketHistory]:
        start = perf_counter()
        logger.info(f"Requesting market history for region {region_id}, type {type_id}")
        # Get the market history for the given type_id in the specified region
        data = self.preston.get_op(
            "get_markets_region_id_history",
            region_id=str(region_id),
            type_id=str(type_id),
        )
        logger.info(
            f"Retrieved {len(data)} market history records for region {region_id}, "
            f"type {type_id} in {perf_counter() - start:.6f} seconds."
        )
        return [EAM.MarketHistory(**x) for x in data]

    def get_market_prices_universe(self) -> Sequence[EAM.MarketPricesUniverse]:
        """Get market prices for the entire universe."""
        start = perf_counter()
        logger.info("Requesting market prices for the universe.")
        data: Sequence[dict[str, Any]] = self.preston.get_op("get_markets_prices")  # type: ignore
        logger.info(
            f"Retrieved {len(data)} market prices for the universe in "
            f"{perf_counter() - start:.6f} seconds."
        )
        return import_market_prices_universe(data)

    def get_region_market_types(self, region_id: int) -> Sequence[int]:
        """Get type ids with active market orders for a specific region."""
        start = perf_counter()
        paged_data: Sequence[Sequence[int]] = []
        logger.info(f"Requesting market types for region {region_id}")
        data = self.preston.get_op(
            "get_markets_region_id_types", region_id=str(region_id)
        )
        page_count = int(self.preston.stored_headers[0].get("x-pages", 1))
        paged_data.append(data)  # type: ignore
        logger.info(
            f"Retrieved {len(data)} market types for region {region_id}, "
            f"page 1 of {page_count}"
        )
        for page in range(2, page_count + 1):
            data = self.preston.get_op(
                "get_markets_region_id_types", region_id=str(region_id), page=str(page)
            )
            logger.info(
                f"Retrieved {len(data)} market types for region "
                f"{region_id}, page {page} of {page_count}"
            )
            paged_data.append(data)  # type: ignore
        logger.info(
            f"Total market types retrieved for region {region_id}: "
            f"{sum(len(page) for page in paged_data)} in {perf_counter() - start:.6f} seconds."
        )
        # Flatten the list of lists into a single list of type IDs
        flat_data = list(chain(*paged_data))
        return flat_data

    def get_market_orders(self, region_id: int) -> EAM.MarketOrderDict:
        """Get market orders for a specific region."""
        start = perf_counter()
        result = EAM.MarketOrderDict(region_id=region_id, data={})
        paged_data: Sequence[Sequence[dict[str, Any]]] = []
        logger.info(f"Requesting all market orders for region {region_id}.")
        request_start = perf_counter()
        data = self.preston.get_op(
            "get_markets_region_id_orders", region_id=str(region_id)
        )
        page_count = int(self.preston.stored_headers[0].get("x-pages", 1))
        paged_data.append(data)  # type: ignore
        logger.info(
            f"Retrieved {len(data)} market orders on page 1 of {page_count} for "
            f"region {region_id} in {perf_counter() - request_start:.6f} seconds."
        )
        for page in range(2, page_count + 1):
            request_start = perf_counter()
            data = self.preston.get_op(
                "get_markets_region_id_orders", region_id=str(region_id), page=str(page)
            )
            paged_data.append(data)  # type: ignore
            logger.info(
                f"Retrieved {len(data)} market orders on page {page} of {page_count} "
                f"for region {region_id} in {perf_counter() - request_start:.6f} seconds."
            )
        logger.info(
            f"Total market orders retrieved for region {region_id}: "
            f"{sum(len(page) for page in paged_data)} in "
            f"{perf_counter() - start:.6f} seconds."
        )
        flat_data = chain(*paged_data)
        for item in flat_data:
            order = EAM.MarketOrder(region_id=region_id, **item)
            if order.type_id not in result.data:
                result.data[order.type_id] = []
            result.data[order.type_id].append(order)
        return result
