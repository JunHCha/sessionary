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
            settings.database_url.unicode_string(),
            pool_size=settings.min_connection_count,
            max_overflow=settings.max_connection_count,
            echo=True,
        )
        self._async_session_factory = async_scoped_session(
            async_sessionmaker(
                self._engine,
                expire_on_commit=False,
                autoflush=False,
            ),
            scopefunc=current_task,
        )

    @property
    def engine(self):
        return self._engine

    @asynccontextmanager
    async def async_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self._async_session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
