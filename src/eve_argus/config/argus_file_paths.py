"""File paths to the Argus data files."""

from pathlib import Path


class ArgusFilePaths:
    """File paths to Argus data files."""

    TYPE_INFO = Path("localized-type-info.json")
    TYPE_DESCRIPTION = Path("localized-type-descriptions.json")
    BLUEPRINTS = Path("blueprints.json")
    MARKET_GROUPS = Path("market-groups.json")
    META_GROUPS = Path("meta-groups.json")
    GROUPS = Path("groups.json")
    CATEGORIES = Path("categories.json")
    MARKET_PRICES_UNIVERSE = Path("market-prices-universe.json")
    ESI_DATA = Path("esi-data")
    TYPE_IDS_PUBLISHED = Path("type-ids-published.json")
    TYPE_IDS_IN_BLUEPRINTS = Path("type-ids-in-blueprints.json")
    TYPE_IDS_IN_MARKET = Path("type-ids-in-market.json")
    TYPE_IDS_FOR_INDUSTRY_PRICING = Path("type-ids-for-industry-pricing.json")
    SYSTEM_COST_INDICES = Path("system-cost-indices.json")
    # Template strings
    MARKET_HISTORY = "${region_id}-${type_id}-market-history.json"
    MARKET_HISTORIES = "${region_id}-market-histories.json"
    REGIONAL_MARKET_ORDERS = "${region_id}-market-orders.json"
    MARKET_ORDERS = "${region_id}-${type_id}-market-orders.json"
    MARKET_HISTORY_SUMMARIES = "${region_id}-${tag}-market-history-summaries.json"
    MARKET_ORDER_SUMMARIES = "${region_id}-${tag}-market-order-summaries.json"
