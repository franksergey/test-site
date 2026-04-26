# ruff: noqa: TC002, TC003

from collections.abc import AsyncGenerator
from typing import Annotated, cast

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from server.config import settings
from server.database import EmailEntry

INDEX_PAGE_PATH = settings.api.STATICFILES / "index.html"
INDEX_PAGE = INDEX_PAGE_PATH.read_text()

router = APIRouter()


@router.get("/")
async def read_root() -> HTMLResponse:
    return HTMLResponse(content=INDEX_PAGE)


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    sessionmaker = cast(
        "async_sessionmaker[AsyncSession]", request.state.sessionmaker
    )

    async with sessionmaker.begin() as session:
        yield session


@router.post("/emails", status_code=status.HTTP_201_CREATED)
async def send_emaili(
    db_session: Annotated[AsyncSession, Depends(get_session)], email: str
) -> None:
    db_obj = EmailEntry(email=email)

    db_session.add(db_obj)
    await db_session.flush()


@router.get("/emails")
async def read_email(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> list[str]:
    stmt = select(EmailEntry)
    db_objs = (await db_session.scalars(stmt)).all()

    return [db_obj.email for db_obj in db_objs]
