import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, TypedDict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.config import settings
from server.database import database
from server.site import router as root_router

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

logger = logging.getLogger(__name__)


def setup_app() -> FastAPI:
    logger.info("Создание и настройка объекта FastAPI")
    app = FastAPI(title="Fest Site", lifespan=lifespan)

    setup_routers(app)
    setup_middlewares(app)

    return app


def setup_routers_v1(app: FastAPI) -> None:
    app.include_router(root_router)
    app.mount(
        "/",
        StaticFiles(directory=settings.api.STATICFILES / "1", html=True),
        name="static",
    )


def setup_routers(app: FastAPI) -> None:
    match settings.api.SITEVERSION:
        case "1":
            setup_routers_v1(app)
        case _:
            msg = "Unknown version"
            raise NotImplementedError(msg)


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
    async with database() as sessionmaker:
        yield {"sessionmaker": sessionmaker}
