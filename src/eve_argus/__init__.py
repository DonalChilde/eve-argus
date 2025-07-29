"""Top-level package for eve_argus."""

from pathlib import Path

from typer import get_app_dir

__author__ = "Chad Lowe"
__email__ = "pfmsoft.dev@gmail.com"
__name__ = "Eve Argus"
# The short X.Y.Z version.
__version__ = "0.0.0"
# The full version, including alpha/beta/rc tags.
__release__ = __version__


_config_dir = Path(get_app_dir(__name__, force_posix=True))
CONFIG = {
    "app_name": "Eve Argus",
    "version": __version__,
    "description": "A tool for importing and exporting EVE Online data.",
    "config_dir": _config_dir,
    "default_app_path": _config_dir,
    "default_app_data_path": _config_dir / "app_data",
    "default_esi_data_path": _config_dir / "esi_data",
    "default_sde_path": Path.home() / "projects" / "eve-sde",
    "log_path": _config_dir / "logs",
    "debug_path": _config_dir / "debug",
}
