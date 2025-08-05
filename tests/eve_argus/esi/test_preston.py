"""Tests for the Eve Argus Preston client."""

import logging
from uuid import uuid4

from eve_argus.esi_client.preston.esi_preston import ArgusPreston
from eve_argus.models.esi import EsiAction, EsiRequest, EsiResponse

logger = logging.getLogger(__name__)


def test_paged_request(caplog):
    """Test that paged requests are handled correctly."""
    region_id = 10000002
    preston_client = ArgusPreston()
    esi_request = EsiRequest(
        request_id=uuid4(),
        op_id="get_markets_region_id_types",
        arguments={"region_id": str(region_id)},
    )
    action = EsiAction(request=esi_request)
    preston_client.get_esi_data(action)

    assert action.response is not None
    print(f"Headers for parent request: {action.response.headers!r}")
    # print(f"Data for parent request: {action.response.data!r}")
    assert isinstance(action.response, EsiResponse)
    assert action.response.status_code == 0
    assert len(action.pages) == int(action.response.headers.get("x-pages", 0)) - 1

    logger.info(
        f"Paged request for region {region_id} returned {len(action.pages)} pages."
    )
