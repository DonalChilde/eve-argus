# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "preston",
# ]
# ///
from pathlib import Path
from time import perf_counter
from typing import cast

import preston

from eve_argus.eve_argus_esi.esi_models import MarketHistory
from eve_argus.snippets.file.csv import write_dicts_to_csv

type_ids = [34, 35, 36, 37, 38, 39]
region_id = 10000002  # The Forge region ID
save_path = (
    Path.home() / "projects" / "tmp" / "eve-argus" / "preston-test-market-history"
)


def main() -> None:
    start = perf_counter()
    p = preston.Preston(useragent="preston-test")
    periods = [10, 30, 60, 90]
    for type_id in type_ids:
        print(f"Requesting ({region_id},{type_id})")
        # Get the market history for the given type_id in the Forge region (10000002)
        # This will use the cached response if available

        data = p.get_op(
            "get_markets_region_id_history",
            region_id=str(region_id),
            type_id=str(type_id),
        )
        cast(list[MarketHistory], data)
        file_name = f"{region_id}_{type_id}_market_history.csv"
        file_path = save_path / file_name
        count = write_dicts_to_csv(data=data, file_path=file_path, overwrite=True)
        print(f"Wrote {count} records for ({region_id},{type_id}) to {file_path}")
        print("\n")
    end = perf_counter()
    elapsed = end - start
    print(f"Request took {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()
