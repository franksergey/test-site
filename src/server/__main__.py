import asyncio
import logging
import sys

import uvicorn

from server.config import settings
from server.logging import get_config_path, setup_logging

logger = logging.getLogger(__name__)


def create_asyncio_event_loop() -> asyncio.AbstractEventLoop:
    if sys.platform == "win32":
        import winloop  # noqa: PLC0415

        logger.info("Используется цикл событий winloop.Loop")
        return winloop.new_event_loop()

    if sys.platform == "linux":
        import uvloop  # noqa: PLC0415

        logger.info("Используется цикл событий uvloop.Loop")
        return uvloop.new_event_loop()

    logger.info("Выбор цикла событий предоставляется asyncio")
    return asyncio.new_event_loop()


def launch_server() -> None:
    """Запустить `uvicorn` сервер."""
    logger.info("Производится запуск основного раннера сервера.")
    uvicorn.run(
        "server.app:setup_app",
        factory=True,
        host=settings.api.HOST,
        port=settings.api.PORT,
        reload=settings.api.RELOAD,
        reload_dirs=["src", "static"],
        reload_includes=["*.*"],
        reload_excludes=["__pycache__", "*.pyc", "*.log", "*.lock", ".git"],
        log_config=get_config_path(),
        log_level="debug",
        use_colors=True,
        loop="server.__main__:create_asyncio_event_loop",
    )


def main() -> None:
    setup_logging()
    launch_server()


if __name__ == "__main__":
    main()
