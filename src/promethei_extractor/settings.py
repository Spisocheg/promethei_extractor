import sys
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class ExtractorSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    login: str = Field(validation_alias='PROMETHEI_LOGIN', min_length=1)
    password: str = Field(validation_alias='PROMETHEI_PASS', min_length=1)
    output_dir: Path = Field(default_factory=Path.cwd)


class _LazySettings:
    _instance: ExtractorSettings | None = None

    def __getattr__(self, item):
        if self._instance is None:
            self._instance = ExtractorSettings()    # noqa
        return getattr(self._instance, item)


settings: ExtractorSettings = _LazySettings()   # type: ignore[assignment]


def init_logger(level: str = 'INFO'):
    logger.remove()
    frmt = '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>[{name}] {message}</level>'
    logger.add(sys.stderr, format=frmt, level=level)
