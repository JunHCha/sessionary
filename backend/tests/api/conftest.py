from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.manager import UserManager
from app.core.auth.strategy import AuthSessionSchema
from app.core.settings.base import AppSettings
from app.db.tables import User
from app.user.models import Subscription
from tests.mock.redis_mock import RedisMock


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
async def test_user(user_manager_stub: UserManager):
    from fastapi_users.schemas import BaseUserCreate

    user_create = BaseUserCreate(
        email="test@test.com",
        password="password",
        is_superuser=False,
        is_active=True,
    )
    user = await user_manager_stub.create(user_create)

    return user


@pytest.fixture
async def test_artist(user_manager_stub: UserManager, test_session: AsyncSession):
    from fastapi_users.schemas import BaseUserCreate

    user_create = BaseUserCreate(
        email="artist@test.com",
        password="password",
        is_superuser=False,
        is_active=True,
    )
    user = await user_manager_stub.create(user_create)
    user.is_artist = True
    await test_session.flush()

    return user


@pytest.fixture
async def test_admin(user_manager_stub: UserManager):
    from fastapi_users.schemas import BaseUserCreate

    user_create = BaseUserCreate(
        email="admin@test.com",
        password="password",
        is_superuser=True,
        is_active=True,
    )
    user = await user_manager_stub.create(user_create)

    return user


@pytest.fixture
def make_authorized_client(
    client: AsyncClient, auth_redis: RedisMock, test_settings: AppSettings
):
    async def _make_client(user: User, session: AsyncSession, token: str):
        async with session:
            user = await session.merge(user)
            await auth_redis.setex(
                f"auth-session-id:{token}",
                test_settings.auth_session_expire_seconds,
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
            )
            client.cookies.set("satk", token)
        return client

    return _make_client


@pytest.fixture
async def authorized_client(
    make_authorized_client, test_user, test_session: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
    client = await make_authorized_client(test_user, test_session, token="SESSIONTOKEN")
    yield client


@pytest.fixture
async def authorized_client_artist(
    make_authorized_client, test_artist, test_session: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
    client = await make_authorized_client(
        test_artist, test_session, token="SESSIONTOKEN_ARTIST"
    )
    yield client


@pytest.fixture
async def authorized_client_admin(
    make_authorized_client, test_admin, test_session: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
    client = await make_authorized_client(
        test_admin, test_session, token="SESSIONTOKEN_ADMIN"
    )
    yield client
