"""
Настройки проекта.
"""


from pydantic import BaseSettings


class Settings(BaseSettings):

    # путь к директории для сохранения файлов
    MEDIA_PATH: str = "../media"

    # путь к директории для логирования
    LOGGING_PATH: str = "../logs"
    # формат для записей логов
    LOGGING_FORMAT: str = "%(name)s %(asctime)s %(levelname)s %(message)s"

    # уровень логирования
    LOGGING_LEVEL: str = "INFO"

    # ключи для доступа к API
    API_KEY_APILAYER: str
    API_KEY_OPENWEATHER: str

    # время актуальности данных о странах (в секундах), по умолчанию – один год
    CACHE_TTL_COUNTRY: int = int("31_536_000")
    # время актуальности данных о курсах валют (в секундах), по умолчанию – сутки
    CACHE_TTL_CURRENCY_RATES: int = int("86_400")
    # время актуальности данных о погоде (в секундах), по умолчанию ~ три часа
    CACHE_TTL_WEATHER: int = int("10_700")


settings = Settings(_env_file="../.env")
