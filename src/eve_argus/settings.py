"""Settings module for Eve Argus."""

from typing import NotRequired, TypedDict

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from eve_argus import DEFAULT_APP_DIR, __app_name__, __description__, __version__

_app_env_prefix = "PFMSOFT_EVE_ARGUS_"


class ConfigDict(TypedDict):
    """Configuration dictionary type for Eve Argus settings.

    Use this dict when passing settings values through the get_settings() function.
    This is useful for testing purposes, and for overriding settings in different environments.
    e.g. Using the app from a third party package.
    """

    config_dir: NotRequired[str]
    log_path: NotRequired[str]
    sde_base_url: NotRequired[str]
    sde_latest_info: NotRequired[str]
    sde_file_template: NotRequired[str]
    sde_schema_changelog_url: NotRequired[str]


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
    sde_base_url: str = Field(
        default="https://developers.eveonline.com/static-data",
        description="The base URL to download the latest SDE data.",
    )
    sde_latest_info: str = Field(
        default="/tranquility/latest.jsonl",
        description="The URL to get information about the latest SDE data.",
    )
    sde_file_template: str = Field(
        default="/tranquility/eve-online-static-data-${build_number}-${variant}.zip",
        description="The URL template to download the SDE data file. build-number can be any valid build number or latest. variant can be jsonl or yaml",
    )
    sde_schema_changelog_url: str = Field(
        default="https://developers.eveonline.com/static-data/tranquility/schema-changelog.yaml",
        description="The URL to get the SDE schema changelog.",
    )


def get_settings(config_dict: ConfigDict | None = None, **kwargs) -> EveArgusSettings:
    """Get the Eve Argus settings with optional configuration overrides.

    This function creates and returns an EveArgusSettings instance, optionally
    merging configuration from a dictionary and keyword arguments.

    Argumanets passed in via get_settings() take precedence over those in env files,
    or the os env.

    Args:
        config_dict (ConfigDict | None, optional): A dictionary containing
            configuration settings. If provided, these settings are used as
            the base configuration. Defaults to None.
        **kwargs: Additional keyword arguments that override or supplement
            the config_dict settings. These take precedence over config_dict
            values for duplicate keys.

    Returns:
        EveArgusSettings: An instance of EveArgusSettings configured with
            the merged settings from config_dict and kwargs, or default
            settings if neither is provided.

    Examples:
        >>> settings = get_settings()  # Use default settings
        >>> settings = get_settings(config_dict={"key": "value"})
        >>> settings = get_settings(key="value", another_key="another_value")
        >>> settings = get_settings(config_dict={"key": "value"}, key="override")
    """
    """Get the Eve Argus settings."""
    combined_kwargs = config_dict.copy() if config_dict else {}
    combined_kwargs.update(kwargs)
    if combined_kwargs:
        return EveArgusSettings(**combined_kwargs)
    return EveArgusSettings()
