from pathlib import Path

import typer

from .batch import app as batch_app
from .cache import app as cache_app
from .get import app as get_app
from .post import app as post_app
from .schema import app as schema_app

app = typer.Typer()
app.add_typer(schema_app, name="schema", help="Schema related commands.")
app.add_typer(batch_app, name="batch", help="Batch related commands.")
app.add_typer(cache_app, name="cache", help="Cache related commands.")
app.add_typer(get_app, name="get", help="Get related commands.")
app.add_typer(post_app, name="post", help="Post related commands.")


if __name__ == "__main__":
    app()
