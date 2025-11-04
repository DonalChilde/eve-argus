"""Command-line interface."""

from time import perf_counter_ns
from typing import Annotated

import typer

from eve_argus import CONFIG
from eve_argus.argus_sde.cli.sde import app as sde_app
from eve_argus.eve_argus_esi.cli.esi import app as esi_app

# from eve_argus.cli.data_exports import app as exports_app
# from eve_argus.cli.data_imports import app as imports_app
# from eve_argus.cli.esi_requests import app as esi_app


def default_options(
    ctx: typer.Context,
    debug: Annotated[bool, typer.Option(help="Enable debug output.")] = False,
    verbosity: Annotated[int, typer.Option("-v", help="Verbosity.", count=True)] = 1,
):
    """Eve Argus Command Line Interface.

    Insert pithy saying here
    """
    ctx.ensure_object(dict)
    ctx.obj["START_TIME"] = perf_counter_ns()
    ctx.obj["DEBUG"] = debug
    ctx.obj["VERBOSITY"] = verbosity
    # Where to init EveArgus? here or in commands?
    # Can i change the data paths for the app in the commands?
    # Since each run of the cli tool is independent, I think it makes sense to
    # initialize the class in the command, so that the option of independent action is there.

    if ctx.obj["VERBOSITY"] > 1:
        typer.echo("App configuration:")
        typer.echo(f"{debug=}")
        typer.echo(f"{verbosity=}")
        typer.echo(f"{CONFIG=!r}")


app = typer.Typer(callback=default_options)

# app.add_typer(exports_app, name="exports", help="Data exports commands.")
# app.add_typer(imports_app, name="imports", help="Data imports commands.")
app.add_typer(esi_app, name="esi", help="ESI requests commands.")
app.add_typer(sde_app, name="sde", help="SDE related commands.")

if __name__ == "__main__":
    app()
