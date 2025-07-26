import logging
from time import perf_counter

from eve_argus.esi import EsiPublic

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_get_market_orders():
    """Test the retrieval of market orders."""
    esi = EsiPublic()
    region_id = 10000002  # The Forge region ID
    market_orders = esi.get_market_orders_by_region(region_id=region_id)
    logger.info("Should hit cache")
    market_orders = esi.get_market_orders_by_region(region_id=region_id)

    assert len(market_orders.orders) > 0, "Expected at least one market order"
