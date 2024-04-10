from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_app_settings


@pytest.fixture
async def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
async def test_user(test_session: AsyncSession):
    from app.db.tables import User

    user = User(
        email="test@test.com",
        nickname="test",
        hashed_password="password",
        is_artist=False,
        is_superuser=False,
        is_active=True,
    )
    async with test_session.begin():
        test_session.add(user)
    await test_session.flush(user)
    return user


@pytest.fixture
async def authorized_client(
    client: AsyncClient, test_user
) -> AsyncGenerator[AsyncClient, None]:
    auth_redis = Redis.from_url(
        get_app_settings().auth_redis_url, decode_responses=True, socket_timeout=1
    )
    await auth_redis.set("auth-session-id:SESSIONTOKEN", str(test_user.id))
    client.headers = {"authorization": "bearer SESSIONTOKEN"}
    yield client
    await auth_redis.flushdb()
