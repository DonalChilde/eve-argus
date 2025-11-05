"""Helper function to read JSONL files."""

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any


def read_jsonl_dicts(
    file_path: Path, encoding: str = "utf-8"
) -> Iterable[dict[str, Any]]:
    """Read a JSONL file and yield each line as a JSON object."""
    with file_path.open("r", encoding=encoding) as f:
        for line in f:
            yield json.loads(line)
