from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Headers
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.strategy import AuthSessionSchema


@pytest.fixture
async def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
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
    await test_session.commit()
    return user


@pytest.fixture
async def authorized_client(
    client: AsyncClient, auth_redis: Redis, test_user
) -> AsyncGenerator[AsyncClient, None]:
    await auth_redis.set(
        "auth-session-id:SESSIONTOKEN",
        AuthSessionSchema.model_validate(test_user).model_dump_json(),
    )
    client.headers = Headers({b"authorization": b"bearer SESSIONTOKEN"})
    yield client
