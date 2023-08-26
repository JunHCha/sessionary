from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings.base import AppSettings


class SessionManager:
    def __init__(self, settings: AppSettings):
        self._engine = create_async_engine(
            settings.db_url,
            pool_size=settings.min_connection_count,
            max_overflow=settings.max_connection_count,
        )
        self._async_session_factory = async_scoped_session(
            async_sessionmaker(self._engine, expire_on_commit=False),
            scopefunc=current_task,
        )

    @asynccontextmanager
    async def async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._async_session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
