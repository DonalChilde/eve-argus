"""Code for importing data from SDE to Argus models."""

from pathlib import Path

from eve_argus.data_transform import sde_to_argus as DI
from eve_argus.file_io.argus_data_file_writer import ArgusFileWriter
from eve_argus.file_io.sde_reader import SdeReader


def import_data_from_sde(
    sde_path: Path,
    argus_path: Path,
    lang: str = "en",
    effective_date: str | None = None,
    sde_version: str | None = None,
) -> None:
    """Import data from SDE to Argus models.

    Args:
        sde_path (Path): Path to the SDE data directory.
        argus_path (Path): Path to the Argus data directory.
        lang (str, optional): Language code for names. Defaults to "en".
        effective_date (str | None, optional): The effective date for the data. Defaults to None.
        sde_version (str | None, optional): The version of the SDE data. Defaults to None.
    """
    # FIXME code to look for effective date and version data here.
    # TODO code to add version information to the argus data files.

    sde_reader = SdeReader(sde_path=sde_path)
    argus_writer = ArgusFileWriter(argus_path=argus_path)

    sde_categories = sde_reader.categories()
    argus_categories = DI.categories(
        sde_categories=sde_categories, effective_date=effective_date, lang=lang
    )
    argus_writer.categories(argus_categories)

    sde_groups = sde_reader.groups()
    argus_groups = DI.groups(
        sde_groups=sde_groups, effective_date=effective_date, lang=lang
    )
    argus_writer.groups(argus_groups)

    sde_meta_groups = sde_reader.meta_groups()
    argus_meta_groups = DI.meta_groups(
        sde_meta_groups=sde_meta_groups, effective_date=effective_date, lang=lang
    )
    argus_writer.meta_groups(argus_meta_groups)

    sde_market_groups = sde_reader.market_groups()
    argus_market_groups = DI.market_groups(
        sde_market_groups=sde_market_groups, effective_date=effective_date, lang=lang
    )
    argus_writer.market_groups(argus_market_groups)

    sde_blueprints = sde_reader.blueprints()
    argus_blueprints = DI.blueprints(
        sde_blueprints=sde_blueprints, effective_date=effective_date
    )
    argus_writer.blueprints(argus_blueprints)

    sde_types = sde_reader.types()
    argus_types, argus_descriptions = DI.sde_types(
        sde_types=sde_types,
        sde_groups=sde_groups,
        effective_date=effective_date,
        lang=lang,
    )
    argus_writer.type_infos(argus_types)
    argus_writer.type_descriptions(argus_descriptions)
