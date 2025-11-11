# Eve Argus - A window into EVE Online data.

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Project Description

Eve Argus can download, format, and manipulate data from the EVE Static Data dataset, and the EVE Online ESI.

Version 1 goals:

- Regional market history summaries, with custom time periods.
- Current buy sell 5% for regions, systems, and/or stations.
- Unit cost for manufactured items.
- Industry job status.
- Character inventories.
- Data in json and csv to allow easy import into other programs.
- Saved commands for quick updates of dynamic data.

TODO - Improve usage instructions as program evolves.

## Quick Start

## Usage

## API Usage

## Installation

This project uses uv for development, and uv is also the easiest way to run the project.

> uv docs:  
> [Astral - uv](https://docs.astral.sh/uv/)  
> [https://docs.astral.sh/uv/concepts/tools/](https://docs.astral.sh/uv/concepts/tools/)  
> [https://docs.astral.sh/uv/reference/cli/#uv-tool](https://docs.astral.sh/uv/reference/cli/#uv-tool)  
> [https://docs.astral.sh/uv/pip/packages/#installing-a-package](https://docs.astral.sh/uv/pip/packages/#installing-a-package)  
> [https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-sources](https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-sources)

To run with uv:

> Note the url format for tool install is the same as that for uv pip install:

```bash
# run esi-auth without installing
uvx --from git+https://github.com/DonalChilde/eve-argus@main eve-argus

# OR

# Install to Path
uv tool install --from git+https://github.com/DonalChilde/eve-argus@main eve-argus
# and run
eve-argus ARGS
```

## Development

### Download the source code:

```bash
git clone https://github.com/DonalChilde/eve-argus.git
cd eve-argus
uv sync
# activate the venv if desired
source ./.venv/bin/activate
```

### Use as a dependency in another project:

```toml
# in your pyproject.toml file, for a uv managed project
dependencies = ["eve-argus"]
[tool.uv.sources]
eve-argus = { git = "https://github.com/DonalChilde/eve-argus", branch = "main" }
```

### ruff settings for formatting and linting

```toml
[tool.ruff.lint]
select = ["B", "UP", "D", "DOC", "FIX", "I", "F401"]
# non-imperative-mood (D401)
ignore = ["D401", "D101"]
# extend-select = ["I"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
docstring-code-format = true
docstring-code-line-length = 88
```

## Contributing

## License

MIT License - see LICENSE file for details.

## Support

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
