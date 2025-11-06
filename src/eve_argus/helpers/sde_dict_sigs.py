"""Helper to generate TypedDict definitions from SDE data, and save them to a file."""

import json
from pathlib import Path
from typing import TypedDict

from eve_argus.helpers.dict_diagnostics import (
    RecursiveKeyInfo,
    collect_dict_keys_and_types_recursive,
)
from eve_argus.sde.raw_jsonl_access import RawJsonAccess, SdeFileNames


class SdeDictSigs(TypedDict):
    build_number: str
    files: dict[str, RecursiveKeyInfo]


def gather_sde_dict_sigs(
    sde_directory: Path, build_number: str = "UNDEFINED"
) -> SdeDictSigs:
    """Generate dict sigs from SDE data."""
    files = list(SdeFileNames)

    access = RawJsonAccess(sde_directory=sde_directory)
    result_sigs: SdeDictSigs = {"build_number": build_number, "files": {}}
    for file_name_enum in files:
        data_iter = access.jsonl_iter(file_name_enum)
        key_info = collect_dict_keys_and_types_recursive(
            data_iter, source_info=f"SDE file: {file_name_enum}, build: {build_number}"
        )
        result_sigs["files"][file_name_enum] = key_info

    return result_sigs


def sde_dict_sigs_to_file(
    sde_directory: Path, output_file: Path, build_number: str = "UNDEFINED"
):
    """Generate dict sigs from SDE data."""
    sigs = gather_sde_dict_sigs(sde_directory=sde_directory, build_number=build_number)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(sigs, f, indent=2)
