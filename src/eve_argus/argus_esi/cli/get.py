import typer

app = typer.Typer()


@app.command()
def get():
    """Get a resource."""
    typer.echo("Getting resource.")
    # operation, parameters, output choices.
    # allow multiple output choices, eg. json, csv, json with headers, etc.


if __name__ == "__main__":
    app()
