# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "preston",
# ]
# ///
import preston
from time import perf_counter
from pathlib import Path
from eve_argus.util.esi_util import market_history_save_to_csv
type_ids = [34, 35, 36, 37, 38, 39]
region_id = 10000002  # The Forge region ID
save_path = Path.home()/"projects"/"tmp"/"eve-argus"/"preston-test-market-history"

def main() -> None:
    start=perf_counter()
    p = preston.Preston(useragent="preston-test")
    for type_id in type_ids:
        print(f"Requesting type_id {type_id}")
        # Get the market history for the given type_id in the Forge region (10000002)
        # This will use the cached response if available
        
        data = p.get_op('get_markets_region_id_history', region_id=str(region_id), type_id=str(type_id))
        market_history_save_to_csv(region_id, type_id, data, save_path)
        print(p.stored_headers[0])
        print("\n")
    end = perf_counter()
    elapsed = end - start
    print(f"Request took {elapsed:.6f} seconds")
    

if __name__ == "__main__":
    main()
