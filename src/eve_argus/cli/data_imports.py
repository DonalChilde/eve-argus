from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def sde(
    ctx: typer.Context, path_in: Annotated[Path, typer.Argument(help="file to import.")]
):
    """Import SDE data from files."""
    pass
    # Placeholder for the actual import logic
