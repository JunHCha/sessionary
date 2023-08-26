from fastapi import Depends
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.manager import UserManager
from app.core.config import get_app_settings
from app.db.tables import AccessToken, OAuthAccount, User
from app.depends.config import get_app_settings

from .db import get_async_session

SETTINGS = get_app_settings()


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
    settings=Depends(get_app_settings),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db, lifetime_seconds=settings.auth_session_expire_seconds
    )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
