import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, TypedDict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from server.config import settings
from server.database import Base
from server.site import read_root

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logger = logging.getLogger(__name__)


def setup_app() -> FastAPI:
    logger.info("Создание и настройка объекта FastAPI")
    app = FastAPI(title="Fest Site", lifespan=lifespan)

    setup_routers(app)
    setup_middlewares(app)

    return app


def setup_routers(app: FastAPI) -> None:
    app.add_api_route("/", read_root, methods=["GET"], tags=["Root"])
    app.mount(
        "/static",
        StaticFiles(directory=settings.api.STATICFILES),
        name="static",
    )


def setup_middlewares(app: FastAPI) -> None:
    """Настройка Middlewares для объекта сервера.

    Args:
        app: Объект сервера.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.debug("Подключено Middleware CORSMiddleware")


class AppInitialState(TypedDict):
    sessionmaker: async_sessionmaker[AsyncSession]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[AppInitialState]:
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
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield {"sessionmaker": sessionmaker}

    await db_engine.dispose()
