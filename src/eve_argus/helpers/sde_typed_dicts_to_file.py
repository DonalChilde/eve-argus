"""Helper to generate TypedDict definitions from SDE data, and save them to a file."""

from dataclasses import dataclass
from pathlib import Path
from pprint import pformat

from eve_argus.helpers.dict_diagnostics import (
    RecursiveKeyInfo,
)
from eve_argus.helpers.sde_dict_sigs import SdeDictSigs, gather_sde_dict_sigs
from eve_argus.sde.raw_jsonl_access import SdeFileNames


def sde_typed_dicts_to_file(
    sde_directory: Path, output_file: Path, build_number: str = "UNDEFINED"
):
    """Generate TypedDict definitions from SDE data."""
    sde_dict_sigs = gather_sde_dict_sigs(
        sde_directory=sde_directory, build_number=build_number
    )
    module_text = make_module(sde_dict_sigs=sde_dict_sigs)
    with output_file.open("w", encoding="utf-8") as f:
        f.write(module_text)


@dataclass(slots=True)
class Attribute:
    name: str
    type: str
    is_optional: bool = False


def make_typed_dict(
    file_name_enum: SdeFileNames, key_info: RecursiveKeyInfo, source_info: str
) -> str:
    """Generate a TypedDict definition from RecursiveKeyInfo."""
    dict_name = f"{file_name_enum.name.replace('_', ' ').title().replace(' ', '')}Dict"
    attributes = collect_attributes(key_info)
    lines: list[str] = []
    lines.append(f"class {dict_name}(TypedDict):")
    lines.append(
        f'    """TypeDict definition for {dict_name}.\n\nTotal entries analyzed: '
        f"{key_info['dict_count']}.\nThis TypedDict was auto-generated and only "
        f"considers top-level keys.\nSource info: {source_info}.\n"
        f"Sig info:\n{pformat(key_info, sort_dicts=True)}.\n"
        f'"""'
    )
    for attr in attributes:
        if attr.is_optional:
            type_str = f"NotRequired[{attr.type}]"
        else:
            type_str = attr.type
        lines.append(f"    {attr.name}: {type_str}")
    return "\n".join(lines)


def collect_attributes(
    key_info: RecursiveKeyInfo,
) -> list[Attribute]:
    """Collect top-level attributes from RecursiveKeyInfo."""
    attributes: list[Attribute] = []
    total_count = key_info["dict_count"]
    keys = list(key_info["key_info"])
    top_level_keys = [key for key in keys if not "." in key]
    for key in top_level_keys:
        types = key_info["key_info"][key]
        type_names = list(types.keys())
        key_count = sum(types.values())
        is_optional = key_count < total_count

        if len(type_names) == 1:
            type_str = type_names[0]
        else:
            type_str = f"Union[{', '.join(type_names)}]"
        attributes.append(Attribute(name=key, type=type_str, is_optional=is_optional))

    return attributes


def make_module(sde_dict_sigs: SdeDictSigs) -> str:
    """Generate a module string containing TypedDict definitions from SdeDictSigs."""
    result_strings = []
    typed_dicts: list[str] = []
    for file_name, key_info in sde_dict_sigs["files"].items():
        sde_file_name = SdeFileNames(file_name)
        typed_dicts.append(
            make_typed_dict(
                file_name_enum=sde_file_name,
                key_info=key_info,
                source_info=f"SDE file: {file_name}, build: {sde_dict_sigs['build_number']}",
            )
        )
    module_docstring = f'''
"""Auto-generated TypedDict definitions for SDE build {sde_dict_sigs["build_number"]}."""

from typing import TypedDict, NotRequired , Union

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


class MaterialsDict(TypedDict):
    typeID: int
    quantity: int


class SkillsDict(TypedDict):
    typeID: int
    level: int


class ProductsDict(TypedDict):
    typeID: int
    quantity: int
    probability: NotRequired[float]


class ActivityDict(TypedDict):
    materials: list[MaterialsDict]
    skills: list[SkillsDict]
    time: int
    products: NotRequired[list[ProductsDict]]


class ActivitiesDict(TypedDict):
    copying: NotRequired[ActivityDict]
    invention: NotRequired[ActivityDict]
    manufacturing: NotRequired[ActivityDict]
    reaction: NotRequired[ActivityDict]
    research_material: NotRequired[ActivityDict]
    research_time: NotRequired[ActivityDict]


class ColorDict(TypedDict):
    b: float
    g: float
    r: float


class MaterialsMateritalsDict(TypedDict):
    """TypeDict definition for MaterialsMateritalsDict.

    This type is used by TypeMaterialsDict. I expect the naming to be fixed in future
    SDE versions, be the same as MaterialsDict.
    """

    materialTypeID: int
    quantity: int

# ------------------------------------------------------------------------------
# File level TypedDict definitions.
# ------------------------------------------------------------------------------

'''
    result_strings.append(module_docstring)
    result_strings.append("\n\n".join(typed_dicts))
    return "\n\n".join(result_strings)
