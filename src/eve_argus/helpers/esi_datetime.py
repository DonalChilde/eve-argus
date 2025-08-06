"""Helper functions for importing datetime strings from ESI responses."""

from datetime import datetime


def import_datetime(data: str) -> str:
    """Import a datetime string from eve esi and return iso 8601 format."""
    # Convert the string to a datetime object
    dt = datetime.strptime(data, "%a, %d %b %Y %H:%M:%S %Z")
    return dt.isoformat()
