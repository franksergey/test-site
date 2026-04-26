import logging

from server.logging import setup_logging

logger = logging.getLogger(__name__)


def launch_server() -> None:
    """Запустить `uvicorn` сервер."""
    logger.info("Производится запуск основного раннера сервера.")
    # TODO(@soucelover)


def main() -> None:
    setup_logging()
    launch_server()


if __name__ == "__main__":
    main()
