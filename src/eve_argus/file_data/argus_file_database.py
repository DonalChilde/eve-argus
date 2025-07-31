"""The API for the argus filebased database."""

from pathlib import Path
from typing import Any

from eve_argus.file_io.argus_data_file_reader import ArgusFileReader
from eve_argus.file_io.argus_data_file_writer import ArgusFileWriter
from eve_argus.models import argus as EAM

# File based data point of entry
# lazy loading of data files
# Stores data from opened files for use.
# check if files are present, and if data is expired.
# report currency of all data


# Consider - Market history download based on market_group, to allow for partial updates
## scenario - an operation requires market history for PI products, the next operation requires minerals and frigates.
## This would allow for a partial update of the market history, rather than downloading all of it.
## restrict this to operations done on the same day, to avoid having data in the same file that has different currency.


# FIXME Add logic to check if the data is expired, and if so, download it again, or notify callers to do so.
## Maybe keep record of expired data, so that callers can check it? A flag has_expired_data could be used for this.


class ArgusData:
    def __init__(self, database_path: Path):
        """Initialize the ArgusData with the path to the database.

        Properties return None if missing, flags self.has_expired_data if data is expired.
        """
        self.database_path = database_path
        self.reader = ArgusFileReader(self.database_path)
        self.writer = ArgusFileWriter(self.database_path)
        self.has_expired_data = False
        self.has_missing_data = False

        self._type_info: EAM.TypeInfos | None = None

        self._market_prices_universe: EAM.UniverseMarketPrices | None = None
        self._system_cost_indices: EAM.SystemCostIndices | None = None
        # self._market_histories: EAM.MarketHistories | None = None

    def _check_for_expired_or_missing(self, value: Any, descriptor: str) -> None:
        """Check if the data is expired."""
        if value is None:
            self.has_missing_data = True
            return None
        # Make a Base class in argus model to hold expiration info?
        self.has_expired_data = False
        return None

    def _update_manifest(self, manifest: Any) -> None:
        """Update the manifest with the current data."""
        # This could be used to update the manifest with the current data.
        # For now, it is a placeholder.
        # Also check for non expired data?
        pass

    ########################## Static data properties ############################

    @property
    def type_info(self) -> EAM.TypeInfos:
        """Get the type info data."""
        if self._type_info is None:
            data = self.reader.type_info()
            self._check_for_expired_or_missing(data, "type_info")
            self._type_info = data
        return self._type_info

    @type_info.setter
    def type_info(self, value: EAM.TypeInfos) -> None:
        """Set the type info data."""
        self._type_info = value
        self._update_manifest(value)
        self.writer.type_infos(value)

    ########################## Dynamic data properties ############################
    @property
    def market_prices_universe(self) -> EAM.UniverseMarketPrices:
        """Get the market prices universe data."""
        if self._market_prices_universe is None:
            data = self.reader.market_prices_universe()
            self._check_for_expired_or_missing(data, "market_prices_universe")
            self._market_prices_universe = data
        return self._market_prices_universe

    @market_prices_universe.setter
    def market_prices_universe(self, value: EAM.UniverseMarketPrices) -> None:
        """Set the market prices universe data."""
        self._market_prices_universe = value
        self._update_manifest(value)
        self.writer.market_prices_universe(value)

    @property
    def system_cost_indices(self) -> EAM.SystemCostIndices:
        """Get the system cost indices data."""
        if self._system_cost_indices is None:
            data = self.reader.system_cost_indices()
            self._check_for_expired_or_missing(data, "system_cost_indices")
            self._system_cost_indices = data
        return self._system_cost_indices

    @system_cost_indices.setter
    def system_cost_indices(self, value: EAM.SystemCostIndices) -> None:
        """Set the system cost indices data."""
        self._update_manifest(value)
        self.writer.system_cost_indices(value)

    # def get_market_history_summaries(

    # def get_market_history(self, region_id: int, type_id: int) -> EAM.MarketHistory:
    #     """Get the market history data."""
    #     if (region_id, type_id) not in self._market_history:
    #         data = self.reader.market_history(region_id, type_id)
    #         self._check_for_expired_or_missing(data, "market_history")
    #         self._market_history[(region_id, type_id)] = data
    #     else:
    #         data = self._market_history[(region_id, type_id)]
    #         self._check_for_expired_or_missing(data, "market_history")
    #     return data

    # def set_market_history(
    #     self, region_id: int, type_id: int, value: EAM.MarketHistory
    # ) -> None:
    #     """Set the market history data."""
    #     self._market_history[(region_id, type_id)] = value
    #     self._update_manifest(value)
    #     self.writer.market_history(region_id, type_id, value)
    # def get_market_histories(self, region_id: int) -> EAM.MarketHistories:
    #     """Get the market histories data."""
    #     if region_id not in self._market_history:
    #         data = self.reader.market_histories(region_id)
    #         self._check_for_expired_or_missing(data, "market_histories")
    #         self._market_history[region_id] = data
    #     else:
    #         data = self._market_history[region_id]
    #         self._check_for_expired_or_missing(data, "market_histories")
    #     data = self.reader.market_histories(region_id)
    #     self._check_for_expired_or_missing(data, "market_histories")
    #     return data
