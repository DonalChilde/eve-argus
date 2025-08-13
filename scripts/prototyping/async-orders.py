# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "aiohttp","eve-argus"
# ]
# ///

import asyncio
from asyncio import Queue
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

import aiohttp

from eve_argus.esi_schema.eve_openapi import EveOpenApi
from eve_argus.eve_argus_esi.esi_models import EsiAction, EsiRequest, EsiResponse
from eve_argus.snippets.aiohttp.queue_simple import AiohttpAction, AiohttpQueueSimple

SPEC_PATH = Path("path/to/openapi/spec.json")  # Adjust this path as needed
ARGUS_DATA_PATH = Path("path/to/argus/data")  # Adjust this path as needed
SESSION = aiohttp.ClientSession()
eve_openapi = EveOpenApi(spec_path=SPEC_PATH)
ESI_BASE_PATH = "https://esi.evetech.net/latest"
IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "TRACE", "PUT", "DELETE"})


## Workflow for esi request:
## 1. Top level function for each request path offers easy sig, e.g get_market_orders(region_id: int)->EAM.MarketOrders
## 2. top level object calls get_op, post_op, etc on EsiClient, passing an EsiAction.
## 3. EsiClient manages requests, responses, errors, and caching for get requests.
## 4. EsiClient.get_op(request:EsiRequest)->EsiResponse:
##    - If the request is cached, it returns the cached response.
##    - If the request is not cached, it makes a new API call and caches the response.
## 5. EsiClient handles pagination and sub-requests automatically.

# TODO build uuid of domain plus url string for cache key.


def get_market_orders(region_id: int, override_cache: bool = False):
    # Placeholder implementation
    print(f"Fetching market orders for region: {region_id}")
    esi_request = EsiRequest(
        request_id=uuid4(),
        op_id="GetMarketsRegionIdOrders",
        method="GET",
        path_params={"region_id": str(region_id)},
    )


def main() -> None:
    print("Hello from async-orders.py!")


if __name__ == "__main__":
    main()
