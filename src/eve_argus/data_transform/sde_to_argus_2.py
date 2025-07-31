# from collections.abc import Sequence
# from typing import Any
# from uuid import uuid4

# from eve_argus.models import argus as EAM


# class TranslateSDEToArgus:
#     def __init__(self, effective_date: str | None, lang: str = "en") -> None:
#         self.effective_date = effective_date
#         self.lang = lang

#     def sde_types_and_descriptions(
#         self,
#         sde_types: dict[int, dict[str, Any]],
#         skip_unpublished: bool = False,
#     ) -> tuple[EAM.TypeInfos, EAM.TypeDescriptions]:
#         """Import TypeInfo from sde, with an optional filter of unpublished items.

#         Split off the description data, and keep only one language. Only keeps fields used
#         by Eve Argus

#         Args:
#             sde_types (dict[int, dict[str, Any]]): The SDE types data.
#             effective_date (str): The effective date for the data.
#             skip_unpublished (bool, optional): If True, skip unpublished types. Defaults to False.
#             lang (str, optional): Two letter language code for localization. Other languages will be dropped. Defaults to "en".

#         Returns:
#             tuple[EAM.TypeInfos, EAM.TypeDescriptions]: Tuple containing TypeInfos and TypeDescriptions.
#         """
#         argus_types = EAM.TypeInfos(
#             data_set_id=uuid4(),
#             effective_date=self.effective_date,
#             description=f"Argus type infos lang={self.lang}",
#             data_source=None,
#             data_type=EAM.DataTypes.Static,
#             data={},
#         )
#         argus_descriptions = EAM.TypeDescriptions(
#             data_set_id=uuid4(),
#             effective_date=self.effective_date,
#             description=f"Argus type descriptions lang={self.lang}",
#             data_source=None,
#             data_type=EAM.DataTypes.Static,
#             data={},
#         )
#         # Iterate over the SDE types and filter based on the skip_unpublished flag
#         # and the specified language.
#         for key, value in sde_types.items():
#             if skip_unpublished:
#                 if value.get("published", False) == False:
#                     continue
#             try:
#                 name = value["name"][self.lang]
#             except KeyError:
#                 name = ""
#             try:
#                 description = value["description"][self.lang]
#             except KeyError:
#                 description = ""
#             argus_types.data[key] = EAM.TypeInfo(
#                 name=name,
#                 type_id=key,
#                 group_id=value.get("groupID", None),
#                 market_group_id=value.get("marketGroupID", None),
#                 meta_group_id=value.get("metaGroupID", None),
#                 graphic_id=value.get("graphicID", None),
#                 capacity=value.get("capacity", None),
#                 portion_size=value.get("portionSize", -1),
#                 published=value.get("published", False),
#             )

#             argus_descriptions.data[key] = EAM.TypeDescription(
#                 type_id=key, description=description
#             )
#         # Return the TypeInfos and TypeDescriptions as a tuple
#         return (argus_types, argus_descriptions)

#     def blueprints(
#         self,
#         sde_blueprints: dict[int, dict[str, Any]],
#     ) -> EAM.Blueprints:
#         """Import blueprints from the SDE.

#         Args:
#             sde_blueprints (dict[int, dict[str, Any]]): Dictionary of blueprint data from SDE.
#             effective_date (str): The effective date for the data.

#         Returns:
#             EAM.Blueprints: Collection of validated Blueprint models.
#         """
#         blueprints = EAM.Blueprints(
#             data_set_id=uuid4(),
#             effective_date=self.effective_date,
#             description=f"Argus blueprints",
#             data_source=None,
#             data_type=EAM.DataTypes.Static,
#             data={},
#         )
#         for sde_item in sde_blueprints.values():
#             bp = EAM.Blueprint.model_validate(sde_item)
#             blueprints.data[bp.blueprintTypeID] = bp
#         return blueprints

#     def market_groups(
#         self,
#         sde_market_groups: dict[int, dict[str, Any]],
#     ) -> EAM.MarketGroups:
#         """Import market groups from the SDE.

#         Args:
#             sde_market_groups (dict[int, dict[str, Any]]): Dictionary of market group data from SDE.
#             effective_date (str): The effective date for the data.
#             lang (str, optional): Language code for names and descriptions. Defaults to "en".

#         Returns:
#             EAM.MarketGroups: Collection of validated MarketGroup models.
#         """
#         market_groups = EAM.MarketGroups(
#             data_set_id=uuid4(),
#             effective_date=self.effective_date,
#             description=f"Argus market groups {self.lang=}",
#             data_source=None,
#             data_type=EAM.DataTypes.Static,
#             data={},
#         )
#         for key, value in sde_market_groups.items():
#             path_id = key
#             parent_path: Sequence[int] = []
#             current = sde_market_groups[path_id]
#             while True:
#                 if path_id is None:
#                     break
#                 parent_path.append(path_id)
#                 path_id = current.get("parentGroupID", None)
#                 if path_id is not None:
#                     current = sde_market_groups[path_id]
#             parent_path.reverse()
#             try:
#                 description = value["descriptionID"][self.lang]
#             except KeyError:
#                 description = ""
#             market_group = EAM.MarketGroup(
#                 group_id=key,
#                 name=value["nameID"][self.lang],
#                 description=description,
#                 has_types=value["hasTypes"],
#                 icon_id=value.get("iconID", -1),
#                 path=tuple(parent_path),
#             )
#             market_groups.data[market_group.group_id] = market_group
#         return market_groups
#     def meta_groups(
#     sde_meta_groups: dict[int, dict[str, Any]],
#     effective_date: str | None = None,
#     lang: str = "en",
# ) -> EAM.MetaGroups:
#     """Import meta groups from the SDE.

#     Args:
#         sde_meta_groups (dict[int, dict[str, Any]]): Dictionary of meta group data from SDE.
#         effective_date (str): The effective date for the data.
#         lang (str, optional): Language code for names. Defaults to "en".

#     Returns:
#         EAM.MetaGroups: Collection of validated MetaGroup models.
#     """
#     argus_meta_groups = EAM.MetaGroups(
#         data_set_id=uuid4(),
#         effective_date=effective_date,
#         description=f"Argus meta groups {lang=}",
#         data_source=None,
#         data_type=EAM.DataTypes.Static,
#         data={},
#     )
#     for key, value in sde_meta_groups.items():
#         meta_group = EAM.MetaGroup(meta_id=key, name=value["nameID"][lang])
#         argus_meta_groups.data[meta_group.meta_id] = meta_group
#     return argus_meta_groups
