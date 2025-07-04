# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "preston",
# ]
# ///
import preston
from time import perf_counter
type_ids = [34, 35, 36, 37, 38, 39]

def main() -> None:
    start=perf_counter()
    p = preston.Preston(useragent="preston-test")
    for type_id in type_ids:
        print(f"Requesting type_id {type_id}")
        # Get the market history for the given type_id in the Forge region (10000002)
        # This will use the cached response if available
        
        data = p.get_op('get_markets_region_id_history', region_id=10000002, type_id=type_id)
        print(p.stored_headers[0])
        print("\n")
    end = perf_counter()
    elapsed = end - start
    print(f"Request took {elapsed:.6f} seconds")
    

if __name__ == "__main__":
    main()
