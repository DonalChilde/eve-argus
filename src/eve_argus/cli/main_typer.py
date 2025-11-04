"""Main CLI Typer app for eve-argus."""

import typer

from eve_argus import __version__
from eve_argus.cli.sde import app as sde_app

app = typer.Typer(no_args_is_help=True)
app.add_typer(sde_app, name="sde", help="SDE related commands.")


@app.command()
def version():
    """Show the eve-argus version."""
    typer.echo(f"eve-argus version: {__version__}")
