import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, TypedDict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logger = logging.getLogger(__name__)


def setup_app() -> FastAPI:
    logger.info("Создание и настройка объекта FastAPI")
    app = FastAPI(title="Fest Site", lifespan=lifespan)

    setup_middlewares(app)

    return app


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
    pass


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[AppInitialState]:
    yield {}
