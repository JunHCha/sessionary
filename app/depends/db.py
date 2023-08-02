from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_app_settings


def get_asyncpg_url(database_url: str) -> str:
    return database_url.replace("postgresql://", "postgresql+asyncpg://")


SETTINGS = get_app_settings()
DATABASE_URL = get_asyncpg_url(SETTINGS.database_url)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
