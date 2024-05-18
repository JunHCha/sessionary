from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionManager
from app.depends.settings import get_app_settings


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_manager = SessionManager(settings=get_app_settings())
    async with session_manager.async_session() as async_session:
        yield async_session
