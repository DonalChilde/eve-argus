import typer

app = typer.Typer()


@app.command()
def post():
    """post to ESI."""
    typer.echo("Posting resource.")
    # operation, parameters, output choices.


if __name__ == "__main__":
    app()
