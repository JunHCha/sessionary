import uuid
from typing import Any

import redis
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
)
from fastapi_users.authentication.strategy import RedisStrategy
from fastapi_users.models import UserProtocol
from httpx_oauth.clients.google import GoogleOAuth2

from app.core.auth.dependancy import get_user_manager
from app.core.settings import get_app_settings
from app.core.settings.base import AppSettings
from app.db.tables import User


class AuthBackend:
    def __init__(self, settings: AppSettings) -> None:
        self.cookie_name = settings.cookie_name
        self.cookie_max_age = settings.auth_session_expire_seconds
        self.cookie_transport = CookieTransport(
            cookie_name=self.cookie_name, cookie_max_age=self.cookie_max_age
        )
        self.bearer_transport = BearerTransport(tokenUrl="/user/auth/login")
        self.auth_session_age = settings.auth_session_expire_seconds
        self.google_client_id = settings.google_client_id
        self.google_client_secret = settings.google_client_secret
        self.auth_redis_url = settings.auth_redis_url

    @property
    def backend(self) -> FastAPIUsers:
        return FastAPIUsers[User, uuid.UUID](get_user_manager, [self.auth_backend])

    @property
    def auth_backend(self) -> AuthenticationBackend[UserProtocol, Any]:
        return AuthenticationBackend(
            name="redis",
            transport=self.bearer_transport,
            get_strategy=self._get_redis_strategy,
        )

    @property
    def google_oauth_client(self) -> GoogleOAuth2:
        return GoogleOAuth2(self.google_client_id, self.google_client_secret)

    def _get_redis_strategy(self) -> RedisStrategy:
        redis_client = redis.asyncio.from_url(
            self.auth_redis_url, decode_responses=True
        )
        return RedisStrategy(
            redis=redis_client,
            lifetime_seconds=self.auth_session_age,
            key_prefix="auth-session-id:",
        )


auth_backend = AuthBackend(settings=get_app_settings())
fastapi_users_component = auth_backend.backend
