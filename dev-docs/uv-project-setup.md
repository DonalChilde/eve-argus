# uv Notes

start with a pyproject.toml with no dependencies.

Generate the project venv

```bash
uv venv
# or with --seed to include pip
uv venv --seed

```

add dependencies like so

```bash
#https://docs.astral.sh/uv/concepts/projects/dependencies/
# Project dependencies
uv add typer

# Optional dependencies
uv add httpx --optional network

# dev dependencies
uv add ruff --dev

# other dependency groups
uv add sphinx --group doc
```