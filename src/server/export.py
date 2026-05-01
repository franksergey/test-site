import asyncio
import logging

from sqlalchemy import select

from server.__main__ import create_asyncio_event_loop
from server.config import settings
from server.database import EmailEntry, database
from server.logging import setup_logging

logger = logging.getLogger(__name__)


async def do_export() -> None:
    async with database() as sessionmaker, sessionmaker() as db_session:
        stmt = select(EmailEntry)
        db_objs = (await db_session.scalars(stmt)).all()

        emails = [db_obj.email for db_obj in db_objs]

    emails = list(dict.fromkeys(emails))
    logger.debug(
        "Получен список email адресов (%r уникальных значений)", len(emails)
    )

    with settings.EXPORTFILE.open("w") as fd:
        fd.write("\n".join(emails))

    logger.info(
        "Все email адреса были экспортированы в %s",
        settings.EXPORTFILE.absolute(),
    )


def main() -> None:
    setup_logging()

    with asyncio.Runner(loop_factory=create_asyncio_event_loop) as runner:
        runner.run(do_export())


if __name__ == "__main__":
    main()
