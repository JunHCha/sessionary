from typing import AsyncGenerator

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionManager


async def get_session(
    session_manager: SessionManager,
) -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.async_session() as session:
        yield session


class DatabaseContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    settings = providers.Dependency()

    session_manager = providers.Singleton(
        SessionManager,
        settings=settings,
    )

    session = providers.Resource(
        get_session,
        session_manager=session_manager,
    )
