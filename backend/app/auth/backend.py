import uuid
from typing import Callable

import redis
from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication.strategy import RedisStrategy
from httpx_oauth.clients.google import GoogleOAuth2

from app.auth.strategy import CustomRedisStrategy, RedisMock
from app.core.settings.base import AppEnv, AppSettings
from app.db.tables import User
from app.user.models import UserRead, UserUpdate


class AuthBackend:
    def __init__(self, settings: AppSettings, get_user_manager: Callable) -> None:
        """
        앱 설정과 사용자 매니저를 바탕으로 인증 관련 구성(쿠키 전송 설정, Redis 인증 백엔드, Google OAuth 클라이언트, FastAPIUsers 컴포넌트)을 초기화한다.
        
        Parameters:
            settings (AppSettings): 다음 필드를 사용하여 구성 값을 제공해야 합니다:
                - app_env: 실행 환경 판단(예: prod, test)
                - cookie_domain: 쿠키 도메인 (값이 "localhost"이면 도메인 없이 설정)
                - cookie_name: 인증 쿠키 이름
                - auth_session_expire_seconds: 세션 만료(초)
                - auth_redis_url: 인증 세션 저장용 Redis URL
                - google_client_id, google_client_secret: Google OAuth 자격 증명
                - google_oauth_redirect_uri: OAuth 리디렉션 URI
            get_user_manager (Callable): FastAPI Users가 사용자 관리를 위해 호출하는 팩토리/콜러블. 이 값을 사용해 FastAPIUsers 컴포넌트를 생성한다.
        """
        self.app_env = settings.app_env
        cookie_secure = self.app_env == AppEnv.prod
        cookie_domain = settings.cookie_domain if settings.cookie_domain != "localhost" else None
        self.cookie_transport = CookieTransport(
            cookie_name=settings.cookie_name,
            cookie_max_age=settings.auth_session_expire_seconds,
            cookie_domain=cookie_domain,
            cookie_secure=cookie_secure,
            cookie_httponly=True,
            cookie_samesite="lax",
        )
        self.auth_session_age = settings.auth_session_expire_seconds

        self.auth_redis_url = settings.auth_redis_url
        self.auth_backend = AuthenticationBackend(
            name="redis",
            transport=self.cookie_transport,
            get_strategy=self.get_redis_strategy,
        )

        self.google_client_id = settings.google_client_id
        self.google_client_secret = settings.google_client_secret
        self.google_oauth_client = GoogleOAuth2(
            self.google_client_id, self.google_client_secret
        )
        self.google_oauth_redirect_uri = settings.google_oauth_redirect_uri

        self.components = FastAPIUsers[User, uuid.UUID](
            get_user_manager, [self.auth_backend]
        )

    @property
    def authenticate_router(self) -> APIRouter:
        return self.components.get_auth_router(self.auth_backend)

    @property
    def oauth_router(self) -> APIRouter:
        return self.components.get_oauth_router(
            self.google_oauth_client,
            self.auth_backend,
            redirect_url=self.google_oauth_redirect_uri,
            state_secret="SECRET",  # TODO: 정확한 사용법을 확인 후 수정
            associate_by_email=True,
        )

    @property
    def password_reset_router(self) -> APIRouter:
        return self.components.get_reset_password_router()

    @property
    def users_router(self) -> APIRouter:
        return self.components.get_users_router(
            user_schema=UserRead, user_update_schema=UserUpdate
        )

    def get_redis_strategy(self) -> RedisStrategy:
        if self.app_env == AppEnv.test:
            redis_client = RedisMock()
        else:
            redis_client = redis.asyncio.from_url(
                self.auth_redis_url,
                decode_responses=True,
            )
        return CustomRedisStrategy(
            redis=redis_client,
            lifetime_seconds=self.auth_session_age,
            key_prefix="auth-session-id:",
        )