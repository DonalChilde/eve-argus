from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def sde(
    ctx: typer.Context,
    path_out: Annotated[Path, typer.Argument(help="directory to export to.")],
):
    """Export SDE data to files."""
    pass
    # Placeholder for the actual export logic
