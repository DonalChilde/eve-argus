"""Helper to generate TypedDict definitions from SDE data, and save them to a file."""

import json
from pathlib import Path
from pprint import pformat

from eve_argus.helpers.dict_diagnostics import (
    collect_dict_keys_and_types,
    collect_dict_keys_and_types_recursive,
    make_typed_dict_definition,
)
from eve_argus.sde.raw_jsonl_access import RawJsonAccess, SdeFileNames


def sde_dict_sigs_to_file(
    sde_directory: Path, output_file: Path, build_number: str = "UNDEFINED"
):
    """Generate dict sigs from SDE data."""
    files = list(SdeFileNames)

    access = RawJsonAccess(sde_directory=sde_directory)
    result_sigs = {}
    result_sigs["BUILD_NUMBER"] = build_number
    for file_name_enum in files:
        data_iter = access.jsonl_iter(file_name_enum)
        key_info = collect_dict_keys_and_types_recursive(
            data_iter, source_info=f"SDE file: {file_name_enum}, build: {build_number}"
        )
        result_sigs[file_name_enum.name] = key_info

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(result_sigs, f, indent=2)
