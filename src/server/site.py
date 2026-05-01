# ruff: noqa: TC002, TC003

import datetime
from collections.abc import AsyncGenerator
from typing import Annotated, cast

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from server.config import settings
from server.database import EmailEntry

INDEX_PAGE_PATH = settings.api.STATICFILES / "index.html"
INDEX_PAGE = INDEX_PAGE_PATH.read_text(encoding="utf-8")

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


@router.post("/emails")
async def send_emaili(
    db_session: Annotated[AsyncSession, Depends(get_session)],
    email: Annotated[str, Form()],
) -> RedirectResponse:
    now = datetime.datetime.now(tz=datetime.UTC)
    db_obj = EmailEntry(email=email, created_at=now)

    db_session.add(db_obj)
    await db_session.flush()

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
