"""SDE CLI commands for eve-argus."""

import asyncio

import typer
from rich.console import Console

from eve_argus.helpers.download_file import get_json_async
from eve_argus.settings import get_settings

app = typer.Typer(no_args_is_help=True)

# TODO: Refactor to reflect the fact that eve-argus no longer uses SDE directly, but might report on it own sde model data.


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
    info, headers = asyncio.run(get_json_async(url=url, headers={}))
    console.print(info)


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
