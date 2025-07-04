# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///
import requests
from time import perf_counter
type_ids = [34, 35, 36, 37, 38, 39]
# The Forge region ID 10000002
def main() -> None:
    start = perf_counter()
    for type_id in type_ids:
        print(f"Requesting type_id {type_id}")
        # Get the market history for the given type_id in the Forge region (10000002)
        
        payload = {
        "datasource": 'tranquility',
        "type_id": type_id,
    }
        r = requests.get("https://esi.evetech.net/latest/markets/10000002/history/", params=payload)
        print(payload,r)
    end = perf_counter()
    elapsed = end - start
    print(f"Request took {elapsed:.6f} seconds")
    
    # print(r.json())


if __name__ == "__main__":
    main()
