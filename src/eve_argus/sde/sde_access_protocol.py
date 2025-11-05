"""Protocol for SDE access implementations.

The SDE access protocol defines the methods that any SDE access implementation
must provide to interact with the SDE data source. This allows for different
implementations to be used interchangeably within the application.

Some possible backends could include:
- Direct file access to the raw SDE jsonl files.
- Access to processed SDE data, such as a database or directory of json files.
"""

from typing import Protocol


class SdeAccessProtocol(Protocol):
    def build_number(self) -> int:
        """Get the SDE build number.

        Returns:
            The SDE build number as an integer.
        """
        ...

    # def release_date(self) -> str:
    #     """Get the SDE release date.

    #     Returns:
    #         The SDE release date as a string in ISO8601 format.
    #     """
    #     ...

    def sde_info(self) -> dict:
        """Get the SDE info as a dictionary.

        Returns:
            The SDE info as a dictionary.
        """
        ...
