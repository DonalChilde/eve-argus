"""Cli commands for importing data."""

from pathlib import Path
from time import perf_counter
from typing import Annotated

import typer

from eve_argus import CONFIG
from eve_argus.argus_sde.argus_sde import import_data_from_sde

app = typer.Typer()


@app.command()
def sde(
    ctx: typer.Context,
    effective_date: Annotated[
        str | None, typer.Option(help="Effective date for the data.")
    ] = None,
    sde_path: Annotated[Path, typer.Option(help="Path to the SDE files.")] = CONFIG[
        "default_sde_path"
    ],
    argus_path: Annotated[
        Path, typer.Option(help="Directory to import SDE data to.")
    ] = CONFIG["default_app_data_path"],
    language: Annotated[
        str,
        typer.Option(
            help="Two letter language code for localization. Other languages will be dropped."
        ),
    ] = "en",
):
    """Import SDE data from files."""
    start = perf_counter()
    typer.echo(
        f"\nImporting SDE data using:\n\tSDE path: {sde_path}\n\tOutput path: {argus_path}"
    )
    typer.echo("\nThis may take over a minute, please be patient.")
    import_data_from_sde(
        sde_path=sde_path,
        argus_path=argus_path,
        lang=language,
        effective_date=effective_date,
    )
    typer.echo(f"\nSDE data imported in {perf_counter() - start:.6f} seconds.\n")


# def type_info_and_descriptions(
#     sde_reader: SdeReader,
#     argus_writer: ArgusFileWriter,
#     effective_date: str | None,
#     lang: str,
# ) -> None:
#     """Get type descriptions from the SDE."""
#     typer.echo("\nImporting types...")
#     start = perf_counter()
#     sde_types = sde_reader.types()
#     typer.echo(f"Loaded {len(sde_types)} types from SDE.")
#     argus_types, argus_descriptions = DI.sde_types(sde_types)
#     argus_writer.type_infos(argus_types)
#     argus_writer.type_descriptions(argus_descriptions)
#     typer.echo(
#         f"Exported {len(argus_types.data)} types and {len(argus_descriptions.data)} "
#         f"descriptions. to {argus_writer.argus_path} in {perf_counter() - start:.6f} seconds."
#     )


# def blueprints(
#     sde_reader: SdeReader, argus_writer: ArgusFileWriter, effective_date: str | None
# ) -> None:
#     """Get blueprints from the SDE."""
#     typer.echo("\nImporting blueprints...")
#     start = perf_counter()
#     sde_blueprints = sde_reader.blueprints()
#     typer.echo(f"Loaded {len(sde_blueprints)} blueprints from SDE.")
#     argus_blueprints = DI.blueprints(sde_blueprints, effective_date=effective_date)
#     argus_writer.blueprints(argus_blueprints)
#     typer.echo(
#         f"Exported {len(argus_blueprints.data)} blueprints to {argus_writer.argus_path} "
#         f"in {perf_counter() - start:.6f} seconds."
#     )


# def market_groups(
#     sde_reader: SdeReader,
#     argus_writer: ArgusFileWriter,
#     effective_date: str | None,
#     lang: str,
# ) -> None:
#     """Get market groups from the SDE."""
#     typer.echo("\nImporting market groups...")
#     start = perf_counter()
#     sde_market_groups = sde_reader.market_groups()
#     typer.echo(f"Loaded {len(sde_market_groups)} market groups from SDE.")
#     argus_market_groups = DI.market_groups(
#         sde_market_groups, effective_date=effective_date, lang=lang
#     )
#     argus_writer.market_groups(argus_market_groups)
#     typer.echo(
#         f"Exported {len(argus_market_groups.data)} market groups to {argus_writer.argus_path} "
#         f"in {perf_counter() - start:.6f} seconds."
#     )


# def meta_groups(
#     sde_reader: SdeReader,
#     argus_writer: ArgusFileWriter,
#     effective_date: str | None,
#     lang: str,
# ) -> None:
#     """Get meta groups from the SDE."""
#     typer.echo("\nImporting meta groups...")
#     start = perf_counter()
#     sde_meta_groups = sde_reader.meta_groups()
#     typer.echo(f"Loaded {len(sde_meta_groups)} meta groups from SDE.")
#     argus_meta_groups = DI.meta_groups(
#         sde_meta_groups, effective_date=effective_date, lang=lang
#     )
#     argus_writer.meta_groups(argus_meta_groups)
#     typer.echo(
#         f"Exported {len(argus_meta_groups.data)} meta groups to {argus_writer.argus_path} "
#         f"in {perf_counter() - start:.6f} seconds."
#     )


# def groups(
#     sde_reader: SdeReader,
#     argus_writer: ArgusFileWriter,
#     effective_date: str | None,
#     lang: str,
# ) -> None:
#     """Get groups from the SDE."""
#     typer.echo("\nImporting groups...")
#     start = perf_counter()
#     sde_groups = sde_reader.groups()
#     typer.echo(f"Loaded {len(sde_groups)} groups from SDE.")
#     argus_groups = DI.groups(sde_groups, effective_date=effective_date, lang=lang)
#     argus_writer.groups(argus_groups)
#     typer.echo(
#         f"Exported {len(argus_groups.data)} groups to {argus_writer.argus_path} "
#         f"in {perf_counter() - start:.6f} seconds."
#     )


# def categories(
#     sde_reader: SdeReader,
#     argus_writer: ArgusFileWriter,
#     effective_date: str | None,
#     lang: str,
# ) -> None:
#     """Get categories from the SDE."""
#     typer.echo("\nImporting categories...")
#     start = perf_counter()
#     sde_categories = sde_reader.categories()
#     typer.echo(f"Loaded {len(sde_categories)} categories from SDE.")
#     argus_categories = DI.categories(
#         sde_categories, effective_date=effective_date, lang=lang
#     )
#     argus_writer.categories(argus_categories)
#     typer.echo(
#         f"Exported {len(argus_categories.data)} categories to {argus_writer.argus_path} "
#         f"in {perf_counter() - start:.6f} seconds."
#     )


# def all(
#     sde_reader: SdeReader,
#     argus_writer: ArgusFileWriter,
#     effective_date: str | None,
#     lang: str,
# ) -> None:
#     """Import all SDE data."""
#     typer.echo("\nImporting all SDE data...")
#     start = perf_counter()
#     type_info_and_descriptions(
#         sde_reader, argus_writer, effective_date=effective_date, lang=lang
#     )
#     blueprints(sde_reader, argus_writer, effective_date=effective_date)
#     market_groups(sde_reader, argus_writer, effective_date=effective_date, lang=lang)
#     meta_groups(sde_reader, argus_writer, effective_date=effective_date, lang=lang)
#     groups(sde_reader, argus_writer, effective_date=effective_date, lang=lang)
#     categories(sde_reader, argus_writer, effective_date=effective_date, lang=lang)
#     typer.echo(f"\nAll SDE data imported in {perf_counter() - start:.6f} seconds.")
