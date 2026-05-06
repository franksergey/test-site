import asyncio
import csv
import io
import smtplib
from email.message import EmailMessage
from typing import TYPE_CHECKING

from sqlalchemy import update

from server.__main__ import create_asyncio_event_loop
from server.config import settings
from server.database import EmailEntry, database

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


async def read_emails(session: AsyncSession) -> Sequence[EmailEntry]:
    stmt = (
        update(EmailEntry)
        .where(EmailEntry.reported.is_(False))
        .values(reported=True)
        .returning(EmailEntry)
    )
    return (await session.scalars(stmt)).all()


def compose_message_content(emails: Sequence[EmailEntry]) -> str:
    with io.StringIO() as buffer:
        buffer.write(
            "Это отчёт со список почт, присланных на наш сервис с момента "
            "последнего отчёта. На каждой строчке выведена почта и через "
            "пробел указанное при отправке имя отправителя в кавычках.\n\n"
        )

        for email in emails:
            buffer.write(f'{email.email} "{email.name}"\n')

        buffer.write(
            "\nВы также можете получить доступ к таблице с отчётом в "
            'прикреплённом файле "report.csv". Он содержит почты, имена и'
            "даты отправки почт в виде таблицы.\n\n"
            "Хорошего вам дня, внезапный почтальон!"
        )

        return buffer.getvalue()


def compose_message_no_emails() -> str:
    return (
        "Это отчёт со список почт, присланных на наш сервис с момента "
        "последнего отчёта. Но почт за этот период никто не прислал, так"
        "что в отчёте, увы, указать нечего.\n\n"
        "Хорошего вам дня, внезапный почтальон!"
    )


def make_message(emails: Sequence[EmailEntry]) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = "Ежедневный отчёт: список отправленных почт"
    msg["To"] = settings.report.TO
    msg["From"] = settings.report.FROM

    if not emails:
        msg.set_content(compose_message_no_emails())
        return msg

    msg.set_content(compose_message_content(emails))

    with io.StringIO() as buffer:
        report_writer = csv.writer(buffer)
        report_writer.writerow(["Email Address", "Name", "Timestamp"])

        for email in emails:
            report_writer.writerow(
                [email.email, email.name, str(email.created_at)]
            )

        csv_report = buffer.getvalue().encode()

    msg.add_attachment(
        csv_report, maintype="text", subtype="csv", filename="report.csv"
    )

    return msg


def send_message(message: EmailMessage) -> None:
    with smtplib.SMTP_SSL(settings.report.SERVER, 465) as smtp:
        smtp.login(settings.report.LOGIN, settings.report.password)
        smtp.send_message(message)


async def make_report() -> None:
    async with database() as sessionmaker, sessionmaker.begin() as session:
        emails = await read_emails(session)
        msg = make_message(emails)
        send_message(msg)


def main() -> None:
    with asyncio.Runner(loop_factory=create_asyncio_event_loop) as runner:
        runner.run(make_report())


if __name__ == "__main__":
    main()
