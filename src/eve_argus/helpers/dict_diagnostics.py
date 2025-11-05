from typing import Iterable, NotRequired, TypedDict

type TypeName = str
type TypeCount = int
type DictTypes = dict[TypeName, TypeCount]
type DictKey = str
type KeyInfo = dict[DictKey, DictTypes]


class DatasetKeyInfo(TypedDict):
    count: int
    key_info: KeyInfo


def collect_dict_keys_and_types(dict_data: Iterable[dict]) -> DatasetKeyInfo:
    """Analyze a list of dictionaries and return the keys and their associated value types.

    Args:
        dict_data: An iterable of dictionaries to analyze.

    Returns:
        A dictionary where each key is a key from the input dictionaries, and the value is another dictionary
        mapping type names to their occurrence counts for that key.
    """
    key_info: KeyInfo = {}
    count = 0
    for entry in dict_data:
        count += 1
        for key, value in entry.items():
            type_name = type(value).__name__
            if key not in key_info:
                key_info[key] = {}
            if type_name not in key_info[key]:
                key_info[key][type_name] = 0
            key_info[key][type_name] += 1
    result: DatasetKeyInfo = {
        "count": count,
        "key_info": key_info,
    }
    return result


def make_typed_dict_definition(
    dict_name: str,
    key_info: DatasetKeyInfo,
) -> str:
    """Generate a TypedDict definition from key information.

    Args:
        dict_name: The name of the TypedDict to generate.
        key_info: The key information as returned by `dict_keys_and_types`.

    Returns:
        A string representing the TypedDict definition.
    """
    lines = [f"class {dict_name}(TypedDict):"]
    doc_string = f"TypeDict definition for {dict_name}.\n\n{' ' * 4}Total entries analyzed: {key_info['count']}.\n{' ' * 4}This TypedDict was auto-generated and only considers top-level keys."
    lines.append(f'{" " * 4}"""{doc_string}\n{" " * 4}"""')
    total_count = key_info["count"]

    for key, types in key_info["key_info"].items():
        type_names = list(types.keys())
        key_count = sum(types.values())
        is_optional = key_count < total_count

        if len(type_names) == 1:
            type_str = type_names[0]
        else:
            type_str = f"Union[{', '.join(type_names)}]"

        if is_optional:
            new_type_str = f"NotRequired\\[{type_str}]"
        else:
            new_type_str = type_str

        lines.append(f"    {key}: {new_type_str}")

    return "\n".join(lines)
