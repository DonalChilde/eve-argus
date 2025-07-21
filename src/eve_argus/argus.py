"""Module for the Eve Argus class."""

import logging
from pathlib import Path

from eve_argus.esi import EsiPublic

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class EveArgus:
    """Main class for Eve Argus operations."""

    def __init__(
        self,
        user_agent: str = "Eve Argus Client",
        debug: bool = False,
        debug_path: Path | None = None,
    ):
        """Initialize the Eve Argus client."""
        self.user_agent = user_agent
        self.debug = debug
        self.debug_path = debug_path
        self.esi_public = EsiPublic(
            user_agent=user_agent, debug=debug, debug_path=debug_path
        )
        logger.info("Eve Argus client initialized.")

    def type_id_to_name(self, type_id: int) -> str:
        """Convert a type ID to its name."""
        # This method would typically query the ESI or a local database
        # to get the name of the type based on its ID.
        # Placeholder implementation for demonstration purposes.
        # FIXME: Replace with actual implementation.
        return f"Type Name for ID {type_id}"
