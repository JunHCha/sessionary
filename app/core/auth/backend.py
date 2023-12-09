import uuid
from typing import Any

import redis
from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication.strategy import RedisStrategy
from fastapi_users.models import UserProtocol
from httpx_oauth.clients.google import GoogleOAuth2

from app.core.auth.manager import UserManager
from app.core.config import get_app_settings
from app.core.settings.base import AppSettings
from app.db.tables import User
from app.depends.db import get_user_db


class AuthBackend:
    def __init__(self, settings: AppSettings = get_app_settings()) -> None:
        self.cookie_name = settings.cookie_name
        self.cookie_max_age = settings.auth_session_expire_seconds
        self.cookie_transport = CookieTransport(
            cookie_name=self.cookie_name,
            cookie_max_age=self.cookie_max_age,
        )
        self.google_client_id = settings.google_client_id
        self.google_client_secret = settings.google_client_secret

    @property
    def backend(self) -> FastAPIUsers:
        return FastAPIUsers[User, uuid.UUID](
            self._get_user_manager, [self.auth_backend]
        )

    @property
    def auth_backend(self) -> AuthenticationBackend[UserProtocol, Any]:
        return AuthenticationBackend(
            name="redis",
            transport=self.cookie_transport,
            get_strategy=self._get_redis_strategy,
        )

    @property
    def google_oauth_client(self) -> GoogleOAuth2:
        return GoogleOAuth2(self.google_client_id, self.google_client_secret)

    def _get_redis_strategy(self) -> RedisStrategy:
        redis_client = redis.asyncio.from_url(
            "redis://auth-redis:6379", decode_responses=True
        )
        return RedisStrategy(
            redis=redis_client,
            lifetime_seconds=self.cookie_max_age,
            key_prefix="auth-session-id:",
        )

    async def _get_user_manager(self, user_db=Depends(get_user_db)):
        yield UserManager(user_db)


auth_backend = AuthBackend(settings=get_app_settings())
fastapi_users_component = auth_backend.backend
