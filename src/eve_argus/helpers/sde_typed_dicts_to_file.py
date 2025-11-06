"""Helper to generate TypedDict definitions from SDE data, and save them to a file."""

from pathlib import Path
from pprint import pformat

from eve_argus.helpers.dict_diagnostics import (
    collect_dict_keys_and_types,
    make_typed_dict_definition,
)
from eve_argus.sde.raw_jsonl_access import RawJsonAccess, SdeFileNames


def sde_typed_dicts_to_file(
    sde_directory: Path, output_file: Path, build_number: str = "UNDEFINED"
):
    """Generate TypedDict definitions from SDE data."""
    files = list(SdeFileNames)

    access = RawJsonAccess(sde_directory=sde_directory)
    result_strings = []
    for file_name_enum in files:
        data_iter = access.jsonl_iter(file_name_enum)
        key_info = collect_dict_keys_and_types(data_iter)
        dict_name = (
            f"{file_name_enum.name.replace('_', ' ').title().replace(' ', '')}Dict"
        )
        typed_dict_def = make_typed_dict_definition(
            dict_name=dict_name,
            key_info=key_info,
            source_info=f"SDE file: {file_name_enum}, build: {build_number}\nKey Info:\n{pformat(key_info, sort_dicts=False)}",
        )

        result_strings.append(typed_dict_def)

    if result_strings and output_file:
        file_header = f'''"""Auto-generated TypedDict definitions for SDE build {build_number}.

At the moment these definitions only consider top-level keys and their types.
"""

from typing import TypedDict, NotRequired

BUILD_NUMBER = {build_number}

# ------------------------------------------------------------------------------
# Sub-level TypedDict definitions.
# ------------------------------------------------------------------------------

class LocalizedStringDict(TypedDict):
    """TypeDict definition for LocalizedStringDict.

    Source info: SDE file: translationLanguages.jsonl, build: 3081406.
    """

    en: str
    de: str
    fr: str
    ja: str
    zh: str
    ru: str
    ko: str
    es: str

# ------------------------------------------------------------------------------
# File level TypedDict definitions.
# ------------------------------------------------------------------------------
        
        '''
        with output_file.open("w", encoding="utf-8") as f:
            f.write(file_header)
            f.write("\n\n".join(result_strings))
