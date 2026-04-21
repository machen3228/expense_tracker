from pathlib import Path
from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict
from pydantic_settings import TomlConfigSettingsSource

if TYPE_CHECKING:
    from tracker.config.database import DatabaseConfig

CONFIGS_ROOT = Path(__file__).parent.parent.parent.parent / "configs"
CONFIG_FILE = CONFIGS_ROOT / "config.toml"
SECRET_FILE = CONFIGS_ROOT / "secret.toml"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file=[CONFIG_FILE, SECRET_FILE],
        env_nested_delimiter="__",
        env_prefix="TRACKER__",
        case_sensitive=False,
        env_ignore_empty=True,
        extra="ignore",
        env_file_encoding="utf-8",
    )

    database: DatabaseConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls, deep_merge=True),
        )


config: Config = Config()
