from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.manager import UserManager
from app.core.auth.strategy import AuthSessionSchema
from app.core.settings.base import AppSettings
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
async def authorized_client(
    client: AsyncClient, auth_redis: RedisMock, test_user, test_settings: AppSettings
) -> AsyncGenerator[AsyncClient, None]:
    await auth_redis.setex(
        "auth-session-id:SESSIONTOKEN",
        test_settings.auth_session_expire_seconds,
        AuthSessionSchema(
            id=test_user.id,
            email=test_user.email,
            nickname=test_user.nickname,
            subscription=Subscription.model_validate(test_user.subscription),
            time_created=test_user.time_created,
            time_updated=test_user.time_updated,
            is_artist=test_user.is_artist,
            is_active=test_user.is_active,
            is_superuser=test_user.is_superuser,
            is_verified=test_user.is_verified,
        ).model_dump_json(),
    )
    client.cookies.set("satk", "SESSIONTOKEN")

    yield client


@pytest.fixture
async def authorized_client_artist(
    client: AsyncClient, auth_redis: RedisMock, test_artist, test_settings: AppSettings
) -> AsyncGenerator[AsyncClient, None]:
    await auth_redis.setex(
        "auth-session-id:SESSIONTOKEN_ARTIST",
        test_settings.auth_session_expire_seconds,
        AuthSessionSchema(
            id=test_artist.id,
            email=test_artist.email,
            nickname=test_artist.nickname,
            subscription=Subscription.model_validate(test_artist.subscription),
            time_created=test_artist.time_created,
            time_updated=test_artist.time_updated,
            is_artist=test_artist.is_artist,
            is_active=test_artist.is_active,
            is_superuser=test_artist.is_superuser,
            is_verified=test_artist.is_verified,
        ).model_dump_json(),
    )
    client.cookies.set("satk", "SESSIONTOKEN_ARTIST")
    yield client


@pytest.fixture
async def authorized_client_admin(
    client: AsyncClient, auth_redis: RedisMock, test_admin, test_settings: AppSettings
) -> AsyncGenerator[AsyncClient, None]:
    await auth_redis.setex(
        "auth-session-id:SESSIONTOKEN_ADMIN",
        test_settings.auth_session_expire_seconds,
        AuthSessionSchema(
            id=test_admin.id,
            email=test_admin.email,
            nickname=test_admin.nickname,
            subscription=Subscription.model_validate(test_admin.subscription),
            time_created=test_admin.time_created,
            time_updated=test_admin.time_updated,
            is_artist=test_admin.is_artist,
            is_active=test_admin.is_active,
            is_superuser=test_admin.is_superuser,
            is_verified=test_admin.is_verified,
        ).model_dump_json(),
    )
    client.cookies.set("satk", "SESSIONTOKEN_ADMIN")
    yield client
