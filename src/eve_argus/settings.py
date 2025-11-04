"""Settings module for Eve Argus."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from eve_argus import DEFAULT_APP_DIR, __app_name__, __description__, __version__

_app_env_prefix = "PFMSOFT_EVE_LINK_"


class EveArgusSettings(BaseSettings):
    """Settings for Eve Argus application."""

    model_config = SettingsConfigDict(
        env_prefix=_app_env_prefix,
        env_file=".eve-argus.env",
        env_file_encoding="utf-8",
    )

    app_name: str = Field(
        default=__app_name__, description="The name of the application."
    )
    version: str = Field(
        default=__version__, description="The version of the application."
    )
    description: str = Field(
        default=__description__,
        description="A brief description of the application.",
    )
    config_dir: str = Field(
        default=f"{DEFAULT_APP_DIR}/config",
        description="The directory where configuration files are stored.",
    )
    log_path: str = Field(
        default=f"{DEFAULT_APP_DIR}/logs",
        description="The directory where log files are stored.",
    )
