"""SDE CLI commands for eve-argus."""

import asyncio
from pathlib import Path
from string import Template
from typing import Annotated, Literal

import typer
from rich.console import Console

from eve_argus.cli.sde_dev import app as sde_dev_app
from eve_argus.helpers.simple_download_async import download_file, download_json
from eve_argus.sde.raw_jsonl_access import RawJsonAccess, SdeFileNames
from eve_argus.settings import get_settings

app = typer.Typer(no_args_is_help=True)
app.add_typer(sde_dev_app, name="dev", help="SDE development commands.")


@app.command(name="info")
def sde_info():
    """Show information about the currently loaded SDE data."""
    console = Console()
    console.print("[bold green]SDE Information[/bold green]")
    console.print("This command will display information about the SDE data.")


@app.command()
def latest():
    """Show information about the latest available SDE data."""
    console = Console()
    console.print("[bold green]Latest SDE Information[/bold green]")
    settings = get_settings()
    url = settings.sde_base_url + settings.sde_latest_info
    console.print(f"The latest SDE data can be found at: {url}")
    info, headers = asyncio.run(download_json(url=url, headers={}))
    console.print(info)


@app.command(name="download")
def download_sde(
    output_dir: Annotated[
        Path,
        typer.Argument(
            help="The directory to save the downloaded SDE data. The file name will be automatically generated, in the form of static-data-{build_number}-{variant}.zip",
            file_okay=False,
        ),
    ],
    variant: Annotated[
        Literal["jsonl", "yaml"],
        typer.Option(
            "-v",
            "--variant",
            help="The variant of the SDE to download",
            show_default=True,
        ),
    ] = "jsonl",
    build_number: Annotated[
        str,
        typer.Option(
            "-b",
            "--build-number",
            help="The build number of the SDE to download",
            show_default=True,
        ),
    ] = "latest",
    overwrite: Annotated[
        bool,
        typer.Option(
            "-o", help="Whether to overwrite existing files", show_default=True
        ),
    ] = False,
):
    """Download the latest SDE data."""
    console = Console()
    console.print("[bold green]Downloading SDE Data...[/bold green]")
    settings = get_settings()
    # Resolve latest build number if needed, because `latest` causes a 403 error.
    if build_number == "latest":
        latest_info_url = f"{settings.sde_base_url}{settings.sde_latest_info}"
        latest_info, _ = asyncio.run(download_json(url=latest_info_url, headers={}))
        build_number = latest_info.get("buildNumber")
        if not build_number:
            console.print(
                "[bold red]Error:[/bold red] Could not resolve latest build number."
            )
            console.print(latest_info)
            raise typer.Exit(code=1)
        console.print(f"Resolved latest build number to: {build_number}")

    url_template = Template(settings.sde_file_template)
    url = f"{settings.sde_base_url}{url_template.substitute(variant=variant, build_number=build_number)}"
    output_path = output_dir / f"static-data-{build_number}-{variant}.zip"
    console.print(f"Downloading SDE data from: {url}")
    headers = asyncio.run(
        download_file(url=url, headers={}, file_path=output_path, overwrite=overwrite)
    )

    console.print("SDE data downloaded successfully.")


@app.command(name="import")
def import_sde():
    """Import SDE data into the system."""
    console = Console()
    console.print("[bold green]Importing SDE Data...[/bold green]")
    settings = get_settings()
    sde_path = settings.sde_file_template
    console.print("SDE data imported successfully.")


@app.command(name="compare")
def compare_sde():
    """Compare current SDE data with the available online version."""
    console = Console()
    console.print("[bold green]Comparing SDE Data...[/bold green]")
    # Placeholder for comparison logic
    console.print("SDE data comparison completed.")


@app.command(name="print")
def print_sde(
    name: Annotated[str, typer.Argument(help="The name of the SDE data to print")],
    sde_directory: Annotated[
        Path,
        typer.Argument(
            help="The directory where the SDE data is located", file_okay=False
        ),
    ],
):
    """Print SDE data to the console."""
    # TODO implement printing specific SDE data by line or range of lines
    # -l line number (repeatable) -s start range -e end range?
    console = Console()
    console.print("[bold green]Printing SDE Data...[/bold green]")
    access = RawJsonAccess(sde_directory=sde_directory)
    try:
        file_name_enum = SdeFileNames[name.upper()]
    except KeyError as e:
        console.print(f"[bold red]Error:[/bold red] Unknown SDE data name: {name}")
        raise typer.Exit(code=1) from e
    data_iter = access.jsonl_iter(file_name_enum)
    for item in data_iter:
        console.print(item)
    # Placeholder for print logic
    console.print("SDE data printed successfully.")
