# from collections.abc import Set
# from pathlib import Path
# from typing import Any

# from yaml import safe_dump, safe_load


# class EveTypes:
#     def __init__(self, localized_types_path: Path) -> None:
#         pass

#     @classmethod
#     def localize_sde_types(
#         cls,
#         sde_types_path: Path,
#         localized_types_path: Path,
#         lang: str = "en",
#         only_published: bool = True,
#     ) -> None:
#         """Remove all but one language from name and description.

#         Args:
#             sde_types_path (Path): _description_
#             localized_types_path (Path): _description_
#             lang (str, optional): _description_. Defaults to "en".
#         """
#         with open(sde_types_path) as file_in:
#             sde_types: dict[int, dict[str, Any]] = safe_load(file_in)
#         print("loaded full SDE.")
#         count = 0
#         skipped = 0
#         for key in list(sde_types.keys()):
#             count += 1
#             if only_published:
#                 if sde_types[key]["published"] == False:
#                     skipped += 1
#                     sde_types.pop(key)
#                     continue
#             sde_types[key] = cls._strip_lang(sde_types[key], lang)
#         localized_types_path.parent.mkdir(parents=True, exist_ok=True)
#         with open(localized_types_path, mode="w") as file_out:
#             safe_dump(sde_types, file_out)
#         print(f"\nProcessed {count} entries, skipping {skipped}")

#     @staticmethod
#     def _strip_lang(type_data: dict[str, Any], lang: str) -> dict[str, Any]:
#         stripped = {}
#         for key in type_data.keys():
#             if key == "name" or key == "description":
#                 localized_data = type_data[key].get(lang, None)
#                 if localized_data is None:
#                     err = ValueError(f"Did not find {lang} in {key} for {type_data!r}")
#                     print(err, "\n")
#                 type_data[key] = {lang: localized_data}
#         return type_data

#     @classmethod
#     def filter_by_typeIDs(
#         cls, sde_types_in: Path, sde_types_out: Path, typeIDs: Set[int]
#     ):
#         with open(sde_types_in) as file_in:
#             full_types = safe_load(file_in)
#         filtered_types = {}
#         for typeID in typeIDs:
#             value = full_types.get(typeID, None)
#             if value is None:
#                 raise ValueError(
#                     f"Tried to get {typeID=} from {sde_types_in} but id not found."
#                 )
#             filtered_types[typeID] = value
#         sde_types_out.parent.mkdir(parents=True, exist_ok=True)
#         with open(sde_types_out, mode="w") as file_out:
#             safe_dump(filtered_types, file_out)
