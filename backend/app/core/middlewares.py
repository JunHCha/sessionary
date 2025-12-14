import orjson
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.auth.backend import AuthBackend
from app.core.settings.base import AppSettings
from app.user.models import AuthSessionSchema


class AuthSessionMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        settings: AppSettings,
        auth_backend: AuthBackend,
    ):
        super().__init__(app)
        self.settings = settings
        self.redis_strategy = auth_backend.get_redis_strategy()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        session_token = request.cookies.get(self.settings.cookie_name)
        if not session_token:
            return await call_next(request)

        redis = self.redis_strategy.redis
        key = f"{self.redis_strategy.key_prefix}{session_token}"
        session_data = await redis.get(key)
        if not session_data:
            return await call_next(request)

        ttl = await redis.ttl(key)
        should_refresh = ttl < (
            self.settings.auth_session_expire_seconds
            - self.settings.auth_session_refresh_interval
        )
        response = await call_next(request)

        if should_refresh:
            new_token = await self.redis_strategy.write_token(
                AuthSessionSchema.model_validate(orjson.loads(session_data))
            )
            await redis.delete(key)
            response.set_cookie(
                self.settings.cookie_name,
                new_token,
                max_age=self.settings.auth_session_expire_seconds,
                httponly=True,
                samesite="lax",
            )

        return response
