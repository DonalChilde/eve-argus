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

import aiohttp

from eve_argus.esi_client.eve_openapi import EveOpenApi
from eve_argus.models.esi import EsiAction, EsiRequest, EsiResponse

SPEC_PATH = Path("path/to/openapi/spec.json")  # Adjust this path as needed
ARGUS_DATA_PATH = Path("path/to/argus/data")  # Adjust this path as needed
SESSION = aiohttp.ClientSession()
eve_openapi = EveOpenApi(spec_path=SPEC_PATH)
ESI_BASE_PATH = "https://esi.evetech.net/latest"
IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "TRACE", "PUT", "DELETE"})


def EsiGetCallback(
    action: EsiAction, queue: Queue
) -> Callable[[aiohttp.ClientResponse, Queue], Awaitable[None]]:
    async def callback(response: aiohttp.ClientResponse, queue: Queue) -> None:
        # TODO implement Argus behaviors here
        ## check response for x-pages
        ## add subactions for pages
        if response.status == 200:
            data = response.json()
            queue.put_nowait(EsiResponse(**data))
        else:
            queue.put_nowait(EsiResponse(error=response.status))

    return callback


def get_market_orders(region_id: int):
    # Placeholder implementation
    print(f"Fetching market orders for region: {region_id}")


def main() -> None:
    print("Hello from async-orders.py!")


if __name__ == "__main__":
    main()
