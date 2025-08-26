from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def batch():
    """Run a batch job."""
    typer.echo("Running batch job.")
    # operation, parameters, output choices.
    # allow multiple output choices, eg. json, csv, json with headers, etc.
    # load a json file describing operations.


if __name__ == "__main__":
    app()
