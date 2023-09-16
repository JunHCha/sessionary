import uuid

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from httpx_oauth.clients.google import GoogleOAuth2
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_app_settings
from app.core.fastapi_users_config.manager import UserManager
from app.db.tables import AccessToken, OAuthAccount, User
from app.depends.db import get_session

settings = get_app_settings()


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_access_token_db(session: AsyncSession = Depends(get_session)):
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


cookie_transport = CookieTransport(
    cookie_name=settings.cookie_name,
    cookie_max_age=settings.auth_session_expire_seconds,
)
auth_backend = AuthenticationBackend(
    name="database",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)
google_oauth_client = GoogleOAuth2(
    settings.google_client_id, settings.google_client_secret
)
fastapi_users_components = FastAPIUsers[User, uuid.UUID](
    get_user_manager, [auth_backend]
)
current_user = fastapi_users_components.current_user()
