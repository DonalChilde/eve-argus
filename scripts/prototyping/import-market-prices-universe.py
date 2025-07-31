# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from pathlib import Path
from time import perf_counter

from eve_argus.data_import.esi_requests import EsiPublic
from eve_argus.file_io.argus_data_file_reader import ArgusFileWriter

EVE_ARGUS_DATA = Path.home() / "projects" / "eve-argus-data"


def main() -> None:
    start = perf_counter()
    esi = EsiPublic()
    print("Hello from import-market-prices-universe.py!")
    data = esi.get_market_prices_universe()
    print(f"Retrieved {len(data)} market prices for the universe.")
    writer = ArgusFileWriter(argus_path=EVE_ARGUS_DATA)
    path_out = writer.market_prices_universe_to_json(market_prices=data)
    print(f"Wrote data for market_prices_universe to {path_out}")
    print(f"Job completed in {perf_counter() - start:.6f} seconds.")


if __name__ == "__main__":
    main()
