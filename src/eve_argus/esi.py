"""API for retrieving public data from Eve ESI."""

from collections.abc import Sequence
import preston
from eve_argus.models import argus as EAM


class EsiPublic:
    def __init__(self, user_agent: str = "Eve Argus testing") -> None:
        self.preston = preston.Preston(user_agent=user_agent)

    def get_market_history(
        self, region_id: int, type_id: int
    ) -> Sequence[EAM.MarketHistory]:
        data = self.preston.get_op(
            "get_markets_region_id_history",
            region_id=str(region_id),
            type_id=str(type_id),
        )
        return [EAM.MarketHistory(**x) for x in data]
