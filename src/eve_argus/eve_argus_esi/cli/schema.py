import typer

app = typer.Typer()


@app.command()
def status():
    """Show the status of the ESI schema."""
    typer.echo("Status of ESI")


@app.command()
def update():
    """Update the ESI schema."""
    typer.echo("Updating ESI schema.")


@app.command()
def get():
    """List the available get operations."""
    # grouped by tag
    # list details determined by a verbose flag.
    # -v list
    # -vv list with descriptions
    # -vvv list, descriptions,example, and schema
    pass


@app.command()
def post():
    """List the available post operations."""
    pass


@app.command()
def detail(operation: str):
    """Show details for a specific operation."""
    typer.echo(f"Showing details for operation: {operation}")


if __name__ == "__main__":
    app()
