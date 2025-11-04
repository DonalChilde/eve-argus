import typer

from .fsd import app as fsd_app

app = typer.Typer()
app.add_typer(fsd_app, name="fsd", help="FSD related commands.")


@app.command()
def sde(name: str):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    app()
