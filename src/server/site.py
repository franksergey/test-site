from fastapi.responses import HTMLResponse

from server.config import settings

INDEX_PAGE_PATH = settings.api.STATICFILES / "index.html"
INDEX_PAGE = INDEX_PAGE_PATH.read_text()


async def read_root() -> HTMLResponse:
    return HTMLResponse(content=INDEX_PAGE)
