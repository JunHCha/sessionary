from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_app_settings
from app.db.tables import AccessToken, User

SETTINGS = get_app_settings()
DATABASE_URL = SETTINGS.database_url

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
