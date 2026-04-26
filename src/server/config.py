from functools import cached_property
from pathlib import Path

from pydantic import BaseModel, DirectoryPath, FilePath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url


class LoggingConfig(BaseModel):
    DOCKER: bool = False


class DatabaseConfig(BaseModel):
    """Конфигурация подключения к базе данных.

    Attributes:
        DIALECT: `$APP_DB_DIALECT`. SQL-диалект. По умолчанию `sqlite`.
        DRIVER: `$APP_DB_DRIVER`. Драйвер для подключения к БД. Должен
            поддерживать асинхронную работу с SQLAlchemy.
        USERNAME: `$APP_DB_USERNAME`. Имя пользователя базы данных.
        PASSWORD: `$APP_DB_PASSWORD`. Пароль для подключения к БД.
        PASSWORDFILE: `$APP_DB_PASSWORDFILE`. Файл с паролем для
            подключения к базе данных.
        HOST: `$APP_DB_HOST`. Адрес хоста базы данных.
        PORT: `$APP_DB_PORT`. Порт для подключения к базе данных.
        DATABASE: `$APP_DB_DATABASE`. Имя базы данных.
        ECHO: `$APP_DB_ECHO`. Если True, SQLAlchemy будет логировать все
            SQL-запросы. Полезно для отладки. По умолчанию False.
        CHECKSCHEMA: `$APP_DB_CHECKSCHEMA`. Проверять схему базы данных
            на расхождения с базой данных? По умолчанию True.
    """

    DIALECT: str = "sqlite"
    DRIVER: str = "aiosqlite"
    USERNAME: str | None = None
    PASSWORD: SecretStr | None = None
    PASSWORDFILE: FilePath | None = None
    HOST: str | None = None
    PORT: int | None = None
    DATABASE: str | None = "./sqlite.db"

    ECHO: bool = False
    CHECKSCHEMA: bool = True

    @cached_property
    def database_url(self) -> URL:
        """DSN (URL) адрес для подключения к БД.

        Автоматически собирает URL-объект из отдельных атрибутов этого
        класса.

        Returns:
            URL адрес для инициализации движка базы данных.
        """
        if self.PASSWORD:
            password = self.PASSWORD.get_secret_value()
        elif self.PASSWORDFILE is not None:
            password = self.PASSWORDFILE.read_text()
        else:
            password = None

        return URL.create(
            drivername=f"{self.DIALECT}+{self.DRIVER}",
            username=self.USERNAME,
            password=password,
            host=self.HOST,
            port=self.PORT,
            database=self.DATABASE,
        )

    @classmethod
    def from_url(
        cls, url: URL | str, *, echo: bool = False, checkschema: bool = True
    ) -> DatabaseConfig:
        url = make_url(url)
        dialect, driver = url.drivername.split("+")

        return DatabaseConfig(
            DIALECT=dialect,
            DRIVER=driver,
            USERNAME=url.username,
            PASSWORD=SecretStr(url.password)
            if url.password is not None
            else url.password,
            HOST=url.host,
            PORT=url.port,
            DATABASE=url.database,
            ECHO=echo,
            CHECKSCHEMA=checkschema,
        )


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
    logging: LoggingConfig = LoggingConfig()
    db: DatabaseConfig = DatabaseConfig()
    api: APIConfig = APIConfig()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        env_nested_delimiter="_",
        extra="ignore",
    )


settings: AppSettings = AppSettings()
