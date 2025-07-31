"""File paths to the Argus data files."""

from enum import StrEnum


class ArgusFilePaths(StrEnum):
    """File paths to Argus data files."""

    # Base directory for categories of Argus data files
    SDE_DATA = "sde-data"
    ESI_DATA = "esi-data"

    #################################
    # Filenames for the data files. #
    #################################

    ###############
    # Static data #
    ###############
    TYPE_INFO = "localized-type-info.json"
    TYPE_INFO_PUBLISHED = "localized-type-info-published.json"
    TYPE_DESCRIPTION = "localized-type-descriptions.json"
    TYPE_DESCRIPTIONS_PUBLISHED = "localized-type-descriptions-published.json"
    BLUEPRINTS = "blueprints.json"
    BLUEPRINTS_PUBLISHED = "blueprints-published.json"
    MARKET_GROUPS = "market-groups.json"
    META_GROUPS = "meta-groups.json"
    GROUPS = "groups.json"
    CATEGORIES = "categories.json"
    TYPE_ID_SUBSETS = "type-id-subsets.json"
    # TYPE_IDS_PUBLISHED = "type-ids-published.json"  # FIXME No longer required?
    # TYPE_IDS_IN_BLUEPRINTS = "type-ids-in-blueprints.json"
    # TYPE_IDS_IN_MARKET = "type-ids-in-market.json"
    # TYPE_IDS_FOR_INDUSTRY_PRICING = "type-ids-for-industry-pricing.json"

    ################
    # Dynamic data #
    ################
    MARKET_PRICES_UNIVERSE = "market-prices-universe.json"
    SYSTEM_COST_INDICES = "system-cost-indices.json"
    # Template strings
    MARKET_HISTORY = "${region_id}-${type_id}-market-history.json"
    MARKET_HISTORIES = "${region_id}-market-histories.json"
    REGIONAL_MARKET_ORDERS = "${region_id}-market-orders.json"
    MARKET_ORDERS = "${region_id}-${type_id}-market-orders.json"
    MARKET_HISTORY_SUMMARIES = "${region_id}-${tag}-market-history-summaries.json"
    MARKET_ORDER_SUMMARIES = "${region_id}-${tag}-market-order-summaries.json"
