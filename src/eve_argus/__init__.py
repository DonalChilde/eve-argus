"""Top-level package for eve_argus."""

from pathlib import Path

from typer import get_app_dir

__author__ = "Chad Lowe"
__author_email__ = "pfmsoft.dev@gmail.com"
__app_name__ = "Eve Argus"
__version__ = "0.1.0"
__license__ = "MIT"
__url__ = "https://github.com/DonalChilde/eve-argus"
__description__ = (
    "A terminal interface for Eve Online information gathering and management."
)

NAMESPACE = "pfmsoft"
APPLICATION_NAME = "esi-link"
DEFAULT_APP_DIR = Path(get_app_dir(f"{NAMESPACE}-{APPLICATION_NAME}"))
USER_AGENT = f"{__app_name__}/{__version__} (+{__url__})"
