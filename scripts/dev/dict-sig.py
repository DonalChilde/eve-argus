from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from eve_argus.helpers.dict_diagnostics import collect_dict_keys_and_types_recursive
from eve_argus.sde.raw_jsonl_access import RawJsonAccess, SdeFileNames

app = typer.Typer(no_args_is_help=True)


@app.command()
def generate(
    sde_directory: Annotated[
        Path, typer.Argument(help="The directory containing the SDE data.")
    ],
    build_number: Annotated[
        str,
        typer.Option("-b", help="The SDE build number of the dataset."),
    ] = "UNDEFINED",
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
        f"[bold green]Generating TypedDict definitions for file: {sde_file} build: {build_number} at: {sde_directory}[/bold green]"
    )
    files = (
        [SdeFileNames[sde_file.upper()]] if sde_file != "ALL" else list(SdeFileNames)
    )
    access = RawJsonAccess(sde_directory=sde_directory)
    # if output_file:
    #     console.print(f"[bold green]Output file: {output_file}[/bold green]")
    #     try:
    #         sde_typed_dicts_to_file(
    #             sde_directory=sde_directory,
    #             output_file=output_file,
    #             build_number=build_number,
    #         )
    #     except Exception as e:
    #         console.print(f"[bold red]Error: {e}[/bold red]")
    #         raise typer.Exit(code=1) from e
    #     return
    for file_name_enum in files:
        data_iter = access.jsonl_iter(file_name_enum)
        key_info = collect_dict_keys_and_types_recursive(data_iter)
        dict_name = (
            f"{file_name_enum.name.replace('_', ' ').title().replace(' ', '')}Dict"
        )
        # typed_dict_def = make_typed_dict_definition(
        #     dict_name=dict_name,
        #     key_info=key_info,
        #     source_info=f"SDE file: {file_name_enum}, build: {build_number}",
        # )

        console.print(f"[bold blue]TypedDict for {file_name_enum}:[/bold blue]")
        console.print(key_info)
        console.print("\n")
