import typer

app = typer.Typer()


@app.command()
def status():
    """Show the status of the cache."""
    typer.echo("Status of cache")


@app.command()
def clear():
    """Clear the cache."""
    typer.echo("Clearing cache")


@app.command()
def clean():
    """Clean the cache of expired data."""
    typer.echo("Cleaning cache")


if __name__ == "__main__":
    app()
