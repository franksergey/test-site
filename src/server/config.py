from pathlib import Path

from pydantic import BaseModel, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIConfig(BaseModel):
    """Конфигурация FastAPI сервера.

    Attributes:
        HOST: `$APP_API_HOST`. Адрес хоста FastAPI сервера.
            По умолчанию `127.0.0.1`.
        PORT: `$APP_API_PORT`. Порт прослушки FastAPI сервера.
            По умолчанию 8000.
        PERFORMCHECKS: `$APP_API_PERFORMCHECKS`. Производить проверки сети
            и провайдеров? По умолчанию да.
        RELOAD: `$APP_API_RELOAD`. Перезагружать сервер при перезаписи
            файлов. По умолчанию да. Избегайте в production образах.
    """

    HOST: str = "127.0.0.1"
    PORT: int = 8000
    PERFORMCHECKS: bool = False
    RELOAD: bool = True
    STATICFILES: DirectoryPath = Path("./static")


class AppSettings(BaseSettings):
    api: APIConfig = APIConfig()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        env_nested_delimiter="_",
        extra="ignore",
    )


settings: AppSettings = AppSettings()
