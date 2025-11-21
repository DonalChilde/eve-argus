# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

import asyncio
from uuid import uuid4

from esi_link.helpers.esi_link_factory import esi_link_factory
from esi_link.models import EsiRequest, EsiRequests
from rich.console import Console


def main() -> None:
    """Execute a test ESI request and print the response.

    This function demonstrates the basic workflow of making an ESI (EVE Swagger Interface)
    request by:
    1. Creating a console for output
    2. Initializing an ESI request for the GetStatus operation
    3. Creating an ESI link via factory
    4. Wrapping the request in an EsiRequests container
    5. Executing the request asynchronously
    6. Printing the JSON response data

    Returns:
        None

    Example:
        >>> main()
        # Prints the JSON response from the ESI GetStatus endpoint
    """
    console = Console()
    request = EsiRequest(request_id=uuid4(), operation_id="GetStatus")
    esi_link = esi_link_factory()
    requests = EsiRequests(requests_id=uuid4(), requests={request.request_id: request})
    responses = asyncio.run(esi_link.execute_requests(requests))
    for key, response in responses.responses.items():
        console.print(
            f"Response status for request ID {key}: {response.http_response.status_code if response.http_response else 'No Response'}"
        )
        console.print(f"\trequest took {response.metrics.request_duration()} seconds")
    http_response = responses.responses[request.request_id].http_response
    if http_response:
        console.print(http_response.json_data)

    # FIXME caching  is not returning the cached value. First call works, subsequent calls return a 304 but no data.


if __name__ == "__main__":
    main()
