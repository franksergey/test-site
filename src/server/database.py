import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import DateTime, MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from server.config import settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей в проекте.

    Он не является таблицей сам по себе, но предоставляет общую
    конфигурацию для всех своих дочерних классов (моделей).

    Attributes:
        metadata: Экземпляр `MetaData` с настроенной конвенцией именования.
            Это гарантирует, что все ключи, индексы и ограничения в базе
            данных будут иметь предсказуемые и единообразные имена.
    """

    metadata: ClassVar[MetaData] = MetaData(
        naming_convention={
            "ix": "ix_%(table_name)s_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": (
                "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
            ),
            "pk": "pk_%(table_name)s",
        }
    )


class EmailEntry(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str]
    name: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    reported: Mapped[bool] = mapped_column(server_default="FALSE")


@asynccontextmanager
async def database() -> AsyncGenerator[async_sessionmaker[AsyncSession]]:
    db_engine = create_async_engine(
        settings.db.database_url,
        echo=settings.db.ECHO,  # Логирование SQL-запросов
        future=True,
        pool_pre_ping=True,  # Проверка соединения перед использованием
    )
    sessionmaker = async_sessionmaker(
        bind=db_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    logger.info("Создан движок БД с DSN адресом %r", settings.db.database_url)

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.debug("Были созданы все таблицы БД через Base.metadata.create_all")

    yield sessionmaker

    await db_engine.dispose()
