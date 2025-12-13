import asyncio
from typing import AsyncGenerator

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.containers.services import ServicesContainer
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


async def get_test_session(
    session_manager: TestSessionManager,
) -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.async_session() as session:
        yield session


class TestDatabaseContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    settings = providers.Singleton(TestAppSettings)

    session_manager = providers.Singleton(
        TestSessionManager,
        settings=settings,
    )

    session = providers.Resource(
        get_test_session,
        session_manager=session_manager,
    )


class TestApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.user.api",
            "app.lecture.api",
        ]
    )

    database = providers.Container(TestDatabaseContainer)

    services = providers.Container(
        ServicesContainer,
        database=database,
    )
