from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionManager
from app.depends.config import get_app_settings


async def get_session(
    settings=Depends(get_app_settings),
) -> AsyncGenerator[AsyncSession, None]:
    session_manager = SessionManager(settings)
    async with session_manager.async_session() as async_session:
        yield async_session
