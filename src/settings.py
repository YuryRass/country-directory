"""
Настройки проекта.
"""

from pathlib import Path
from typing import Any

from pydantic import BaseSettings


class Settings(BaseSettings):
    # базовая директория
    BASE_DIR: Path = Path.cwd().parent
    # название директории для сохранения файлов
    MEDIA_DIR: str = "media"
    # название директории для логирования
    LOGGING_DIR: str = "logs"

    # абсолютные пути до директорий
    MEDIA_ABSOLUTE_PATH: Path = BASE_DIR.joinpath(MEDIA_DIR)
    LOGGING_ABSOLUTE_PATH: Path = BASE_DIR.joinpath(LOGGING_DIR)

    # формат для записей логов
    LOGGING_FORMAT: str = "%(name)s %(asctime)s %(levelname)s %(message)s"

    # уровень логирования
    LOGGING_LEVEL: str = "INFO"

    # ключи для доступа к API
    API_KEY_APILAYER: str
    API_KEY_OPENWEATHER: str
    API_KEY_NEWS: str

    # время актуальности данных о странах (в секундах), по умолчанию – один год
    CACHE_TTL_COUNTRY: int = int("31_536_000")
    # время актуальности данных о курсах валют (в секундах), по умолчанию – сутки
    CACHE_TTL_CURRENCY_RATES: int = int("86_400")
    # время актуальности данных о погоде (в секундах), по умолчанию ~ три часа
    CACHE_TTL_WEATHER: int = int("10_700")
    # время актуаьности новостей о странах (в секундах), по умолчанию - 1 час
    CACHE_TTL_NEWS: int = 3600


def get_settings(**kwargs: Any) -> Settings:
    return Settings(**kwargs)
