import secrets
import time
from typing import Optional

import orjson
import redis.asyncio
from fastapi_users import models
from fastapi_users.authentication.strategy import RedisStrategy
from fastapi_users.manager import BaseUserManager

from app.user.models import AuthSessionSchema, Subscription


class RedisMock:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = {}
            cls._instance.expires = {}
        return cls._instance

    async def set(self, key, value, *args, **kwargs):
        self.data[key] = value
        if "ex" in kwargs:
            self.expires[key] = time.time() + kwargs["ex"]

    async def setex(self, key, seconds, value):
        self.data[key] = value
        self.expires[key] = time.time() + seconds

    async def get(self, key):
        if key in self.expires:
            if time.time() > self.expires[key]:
                del self.data[key]
                del self.expires[key]
                return None
        return self.data.get(key)

    async def ttl(self, key):
        if key not in self.expires:
            return -1
        remaining = int(self.expires[key] - time.time())
        if remaining <= 0:
            del self.data[key]
            del self.expires[key]
            return -2
        return remaining

    async def flushdb(self):
        self.data.clear()
        self.expires.clear()

    async def delete(self, key: str) -> int:
        existed = 0
        if key in self.data:
            del self.data[key]
            existed = 1
        if key in self.expires:
            del self.expires[key]
        return existed


class CustomRedisStrategy(RedisStrategy):
    def __init__(
        self,
        redis: redis.asyncio.Redis | RedisMock,
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
