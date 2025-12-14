import asyncio

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings.test import TestAppSettings
from app.db.session import SessionManager


class TestSessionManager(SessionManager):
    def __init__(self, settings: TestAppSettings):
        self._engine = create_async_engine(
            settings.database_url,
            echo=True,
        )
        self._async_session_factory = async_scoped_session(
            async_sessionmaker(
                self._engine,
                expire_on_commit=False,
                autoflush=False,
            ),
            scopefunc=asyncio.current_task,
        )


class TestDatabaseContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    settings = providers.Dependency()

    session_manager = providers.Singleton(
        TestSessionManager,
        settings=settings,
    )
