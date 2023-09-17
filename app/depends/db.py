from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_app_settings
from app.db.session import SessionManager
from app.db.tables import AccessToken, OAuthAccount, User


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_manager = SessionManager(settings=get_app_settings())
    async with session_manager.async_session() as async_session:
        yield async_session


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_access_token_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
