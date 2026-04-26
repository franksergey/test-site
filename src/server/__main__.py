import asyncio
import logging
import sys

from server.logging import setup_logging

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
    # TODO(@soucelover)


def main() -> None:
    setup_logging()
    launch_server()


if __name__ == "__main__":
    main()
