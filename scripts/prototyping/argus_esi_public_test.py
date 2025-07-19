# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "preston",
# ]
# ///
"""Test the esi public api interface."""

from pathlib import Path
from time import perf_counter

from eve_argus.esi import EsiPublic
from eve_argus.models import argus as EAM
from eve_argus.snippets.file.csv import write_dicts_to_csv
from eve_argus.util.esi import (
    summarize_market_history_by_periods,
)

type_ids = [34, 35, 36, 37, 38, 39]
region_id = 10000002  # The Forge region ID
save_path = Path.home() / "projects" / "tmp" / "eve-argus" / "argus-esi-public-test"


def main() -> None:
    start = perf_counter()
    esi = EsiPublic(debug=True, debug_path=save_path)
    periods = [10, 30, 60, 90]
    for type_id in type_ids:
        print(f"Requesting ({region_id},{type_id})")
        # Get the market history for the given type_id in the Forge region (10000002)
        # This will use the cached response if available

        data = esi.get_market_history(region_id=region_id, type_id=type_id)

        file_name = f"{region_id}_{type_id}_market_history.csv"
        file_path = save_path / file_name
        history_data = (EAM.MarketHistory.model_dump(x) for x in data)
        write_dicts_to_csv(data=history_data, file_path=file_path, overwrite=True)
        print(f"Wrote data for ({region_id},{type_id}) to {file_path}")
        summary = summarize_market_history_by_periods(
            region_id=region_id, type_id=type_id, periods=periods, data=data
        )
        summary_file = save_path / f"{region_id}-{type_id}-market_summary.csv"
        summary_data = (EAM.MarketHistorySummary.model_dump(x) for x in summary)
        summary_count = write_dicts_to_csv(
            data=summary_data, file_path=summary_file, overwrite=True
        )
        print(
            f"Wrote {summary_count} summary records for ({region_id},{type_id}) to {file_path}"
        )

        print("\n")
    end = perf_counter()
    elapsed = end - start
    print(f"Request took {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()
