"""Command-line interface."""

from time import perf_counter_ns
from typing import Annotated

import typer

from eve_argus.cli.data_exports import app as exports_app
from eve_argus.cli.data_imports import app as imports_app
from eve_argus.cli.esi_requests import app as esi_app


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
    typer.echo(f"Verbosity: {verbosity}")
    ctx.obj["VERBOSITY"] = verbosity


app = typer.Typer(callback=default_options)
app.add_typer(exports_app, name="exports", help="Data exports commands.")
app.add_typer(imports_app, name="imports", help="Data imports commands.")
app.add_typer(esi_app, name="esi", help="ESI requests commands.")


# @app.command()
# def hash_md5(
#     ctx: typer.Context, path_in: Annotated[Path, typer.Argument(help="file to hash.")]
# ):
#     hashcode = hash_file(path_in, md5())
#     typer.echo(f"{hashcode}  {path_in.name}")


if __name__ == "__main__":
    app()
