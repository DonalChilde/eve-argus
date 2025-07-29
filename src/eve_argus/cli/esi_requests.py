from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def regional_market_orders(
    ctx: typer.Context,
    region_id: Annotated[int, typer.Argument(help="ID of the region to query.")],
    path_out: Annotated[
        Path | None, typer.Argument(help="directory to export to.")
    ] = None,
):
    """Get regional market orders from esi."""
    pass
    # Placeholder for the actual import logic
