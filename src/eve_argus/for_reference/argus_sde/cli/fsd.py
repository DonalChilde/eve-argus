from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def status():
    """Show the status of the imported FSD data."""
    typer.echo("Status of FSD")


@app.command()
def import_files(file_path: Path):
    """Import FSD files from the given path."""
    typer.echo(f"Importing files from {file_path}")


@app.command()
def export(file_path: Path):
    """Export FSD data to the given path."""
    typer.echo(f"Exporting files to {file_path}")


if __name__ == "__main__":
    app()
