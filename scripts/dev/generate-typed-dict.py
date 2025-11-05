from pathlib import Path
from typing import Annotated, Literal

import typer
from rich.console import Console

from eve_argus.helpers.dict_diagnostics import (
    collect_dict_keys_and_types,
    make_typed_dict_definition,
)
from eve_argus.sde.raw_jsonl_access import RawJsonAccess, SdeFileNames

app = typer.Typer(no_args_is_help=True)


@app.command()
def generate(
    sde_directory: Annotated[
        Path, typer.Argument(help="The directory containing the SDE data.")
    ],
    output_file: Annotated[
        Path | None,
        typer.Option("-f", help="The file to write the generated TypedDicts to."),
    ] = None,
    sde_file: Annotated[
        str,
        typer.Option("-n", help="The SDE file to process."),
    ] = "ALL",
):
    """Generate TypedDict definitions from sample data."""
    pass
    console = Console()
    console.print(
        f"[bold green]Generating TypedDict definitions for {sde_file}...[/bold green]"
    )
    files = (
        [SdeFileNames[sde_file.upper()]] if sde_file != "ALL" else list(SdeFileNames)
    )
    access = RawJsonAccess(sde_directory=sde_directory)
    for file_name_enum in files:
        data_iter = access.jsonl_iter(file_name_enum)
        key_info = collect_dict_keys_and_types(data_iter)
        dict_name = (
            f"{file_name_enum.name.replace('_', '').title().replace(' ', '')}Dict"
        )
        typed_dict_def = make_typed_dict_definition(
            dict_name=dict_name,
            key_info=key_info,
        )
        console.print(f"[bold blue]TypedDict for {file_name_enum.name}:[/bold blue]")
        console.print(typed_dict_def)
        console.print("\n")
