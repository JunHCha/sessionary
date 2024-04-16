import datetime
import secrets
import uuid
from typing import Optional

import orjson
import redis.asyncio
from fastapi_users import models
from fastapi_users.authentication.strategy import RedisStrategy
from fastapi_users.manager import BaseUserManager
from pydantic import BaseModel, ConfigDict


class SessionSchema(BaseModel):
    id: uuid.UUID
    email: str
    nickname: str
    is_artist: bool
    subscription_id: int | None
    time_created: datetime.datetime | None
    time_updated: datetime.datetime | None
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


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

        return SessionSchema.model_validate(user)

    async def write_token(self, user: models.UP) -> str:
        token = secrets.token_urlsafe()
        await self.redis.set(
            f"{self.key_prefix}{token}",
            SessionSchema.model_validate(user).model_dump_json(),
            ex=self.lifetime_seconds,
        )
        return token
