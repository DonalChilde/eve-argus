from eve_argus.argus_sde import fsd_schema as S
from eve_argus.argus_sde import models as M
from eve_argus.argus_sde.fsd_reader import FsdReader


class FsdTranslator:
    def __init__(self, fsd_reader: FsdReader) -> None:
        self.fsd_reader = fsd_reader

    def categories(self) -> M.Categories:
        return _categories(
            self.fsd_reader.get_file("categories"),
            version=self.fsd_reader.manifest.version,
        )

    def meta_groups(self) -> M.MetaGroups:
        return _meta_groups(
            self.fsd_reader.get_file("meta_groups"),
            version=self.fsd_reader.manifest.version,
        )

    def groups(self) -> M.Groups:
        return _groups(
            self.fsd_reader.get_file("groups"),
            version=self.fsd_reader.manifest.version,
        )

    def market_groups(self) -> M.MarketGroups:
        return _market_groups(
            self.fsd_reader.get_file("market_groups"),
            version=self.fsd_reader.manifest.version,
        )

    def type_infos(self) -> tuple[M.TypeInfos, M.TypeDescriptions]:
        type_infos, type_descriptions = _type_infos(
            self.fsd_reader.get_file("type_infos"),
            version=self.fsd_reader.manifest.version,
        )
        return (type_infos, type_descriptions)


def _categories(
    from_fsd: dict[int, S.CategoryTD], version: str, lang: str = "en"
) -> M.Categories:
    """Translate FSD categories to Argus Categories."""
    categories = M.Categories(version=version)
    for category_id, category_data in from_fsd.items():
        category = M.Category(
            category_id=category_id,
            name=category_data["name"][lang],
            published=category_data["published"],
        )
        categories.data[category_id] = category
    return categories


def _meta_groups(
    from_fsd: dict[int, S.MetaGroupTD], version: str, lang: str = "en"
) -> M.MetaGroups:
    """Translate FSD meta groups to Argus MetaGroups."""
    meta_groups = M.MetaGroups(version=version)
    for meta_group_id, meta_group_data in from_fsd.items():
        meta_group = M.MetaGroup(
            meta_id=meta_group_id,
            name=meta_group_data["nameID"][lang],
        )
        meta_groups.data[meta_group_id] = meta_group
    return meta_groups


def _groups(from_fsd: S.Groups, version: str, lang: str = "en") -> M.Groups:
    """Translate FSD groups to Argus Groups."""
    groups = M.Groups(version=version)
    for group_id, group_data in from_fsd.items():
        group = M.Group(
            group_id=group_id,
            anchorable=group_data["anchorable"],
            anchored=group_data["anchored"],
            category_id=group_data["categoryID"],
            fittable_non_singleton=group_data["fittableNonSingleton"],
            icon_id=group_data.get("iconID", -1),
            name=group_data["name"][lang],
            published=group_data["published"],
            use_base_price=group_data["useBasePrice"],
        )
        groups.data[group_id] = group
    return groups


def get_market_group_lineage(
    group_id: int, market_groups: S.MarketGroups
) -> tuple[int, ...]:
    """Return a list of groupIDs representing the parent-child lineage for a given groupID, inclusive.

    The list starts from the root ancestor and ends with the given groupID.
    """
    lineage: list[int] = []
    current_id = group_id
    while current_id is not None:
        lineage.append(current_id)
        group = market_groups.get(current_id)
        if group is None:
            break
        parent_id = group.get("parentGroupID")
        if parent_id is None:
            break
        current_id = parent_id
    return tuple(reversed(lineage))


def _market_groups(
    from_fsd: S.MarketGroups, version: str, lang: str = "en"
) -> M.MarketGroups:
    """Translate FSD market groups to Argus MarketGroups."""
    market_groups = M.MarketGroups(version=version)
    for group_id, group_data in from_fsd.items():
        lineage = get_market_group_lineage(group_id, from_fsd)
        market_group = M.MarketGroup(
            group_id=group_id,
            parent_group_id=group_data.get("parentGroupID"),
            name=group_data["name"][lang],
            description=group_data["description"][lang],
            icon_id=group_data.get("iconID", -1),
            has_types=group_data["hasTypes"],
            path_ids=lineage,
        )
        market_groups.data[group_id] = market_group
    return market_groups


def _type_infos(
    from_fsd: S.TypeInfos, version: str, lang: str = "en"
) -> tuple[M.TypeInfos, M.TypeDescriptions]:
    """Translate FSD type infos to Argus TypeInfos."""
    type_infos = M.TypeInfos(version=version)
    type_descriptions = M.TypeDescriptions(version=version)
    for type_id, type_data in from_fsd.items():
        if "description" not in type_data or lang not in type_data["description"]:
            description = ""
        else:
            description = (type_data["description"][lang],)
        type_descriptions.data[type_id] = M.TypeDescription(
            type_id=type_id,
            description=description,  # pyright: ignore[reportArgumentType]
        )
        if "name" not in type_data or lang not in type_data["name"]:
            name = ""
        else:
            name = type_data["name"][lang]
        type_info = M.TypeInfo(
            name=name,
            type_id=type_id,
            group_id=type_data.get("groupID"),
            category_id=type_data.get("categoryID"),
            market_group_id=type_data.get("marketGroupID"),
            meta_group_id=type_data.get("metaGroupID"),
            graphic_id=type_data.get("graphicID"),
            capacity=type_data.get("capacity"),
            portion_size=type_data.get("portionSize", -1),
            published=type_data["published"],
        )
        type_infos.data[type_id] = type_info
    return (type_infos, type_descriptions)
