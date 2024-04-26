import secrets
from typing import Optional

import orjson
import redis.asyncio
from fastapi_users import models
from fastapi_users.authentication.strategy import RedisStrategy
from fastapi_users.manager import BaseUserManager

from app.subscription.models import Subscription
from app.user.models import AuthSessionSchema


class CustomRedisStrategy(RedisStrategy):
    def __init__(
        self,
        redis: redis.asyncio.Redis,
        lifetime_seconds: Optional[int] = None,
        *,
        key_prefix: str = "fastapi_users_token:",
    ):
        super().__init__(redis, lifetime_seconds, key_prefix=key_prefix)

    async def read_token(
        self, token: Optional[str], user_manager: BaseUserManager[models.UP, models.ID]
    ) -> Optional[models.UP]:
        if token is None:
            return None

        try:
            user = orjson.loads((await self.redis.get(f"{self.key_prefix}{token}")))
        except orjson.JSONDecodeError:
            return None

        if user is None:
            return None

        return AuthSessionSchema.model_validate(user)

    async def write_token(self, user: models.UP) -> str:
        token = secrets.token_urlsafe()
        await self.redis.set(
            f"{self.key_prefix}{token}",
            AuthSessionSchema(
                id=user.id,
                email=user.email,
                nickname=user.nickname,
                subscription=Subscription.model_validate(user.subscription),
                time_created=user.time_created,
                time_updated=user.time_updated,
                is_artist=user.is_artist,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                is_verified=user.is_verified,
            ).model_dump_json(),
            ex=self.lifetime_seconds,
        )
        return token
