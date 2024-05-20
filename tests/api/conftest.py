from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Headers
from redis.asyncio import Redis

from app.core.auth.manager import UserManager
from app.core.auth.strategy import AuthSessionSchema
from app.models import Subscription


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
        is_artist=False,
        is_superuser=False,
        is_active=True,
    )
    user = await user_manager_stub.create(user_create)

    return user


@pytest.fixture
async def test_artist(user_manager_stub: UserManager):
    from fastapi_users.schemas import BaseUserCreate

    user_create = BaseUserCreate(
        email="artist@test.com",
        password="password",
        is_artist=True,
        is_superuser=False,
        is_active=True,
    )
    user = await user_manager_stub.create(user_create)

    return user


@pytest.fixture
async def test_admin(user_manager_stub: UserManager):
    from fastapi_users.schemas import BaseUserCreate

    user_create = BaseUserCreate(
        email="admin@test.com",
        password="password",
        is_artist=False,
        is_superuser=True,
        is_active=True,
    )
    user = await user_manager_stub.create(user_create)

    return user


@pytest.fixture
async def authorized_client(
    client: AsyncClient, auth_redis: Redis, test_user
) -> AsyncGenerator[AsyncClient, None]:
    await auth_redis.set(
        "auth-session-id:SESSIONTOKEN",
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
    client.headers = Headers({b"authorization": b"bearer SESSIONTOKEN"})
    yield client


@pytest.fixture
async def authorized_client_artist(
    client: AsyncClient, auth_redis: Redis, test_artist
) -> AsyncGenerator[AsyncClient, None]:
    await auth_redis.set(
        "auth-session-id:SESSIONTOKEN_ARTIST",
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
    client.headers = Headers({b"authorization": b"bearer SESSIONTOKEN_ARTIST"})
    yield client


@pytest.fixture
async def authorized_client_admin(
    client: AsyncClient, auth_redis: Redis, test_admin
) -> AsyncGenerator[AsyncClient, None]:
    await auth_redis.set(
        "auth-session-id:SESSIONTOKEN_ADMIN",
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
    client.headers = Headers({b"authorization": b"bearer SESSIONTOKEN_ADMIN"})
    yield client
