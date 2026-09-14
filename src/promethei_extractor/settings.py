from pathlib import Path

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExtractorSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    login: str = Field(validation_alias='PROMETHEI_LOGIN')
    password: str = Field(validation_alias='PROMETHEI_PASS')
    output_dir: Path = Field(default_factory=Path.cwd)


settings = ExtractorSettings()  # noqa : способ приведен на оф. сайте
