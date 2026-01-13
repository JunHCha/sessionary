from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi_users.schemas import BaseUserCreate
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.manager import UserManager
from app.auth.strategy import RedisMock
from app.core.settings.test import TestAppSettings
from app.db.tables import User
from app.user.models import AuthSessionSchema, Subscription


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
async def test_user(user_manager_stub: UserManager):
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
    client: AsyncClient,
    auth_redis: RedisMock,
    test_settings: TestAppSettings,
):
    async def _make_client(user: User, session: AsyncSession, token: str):
        async with session:
            from sqlalchemy.orm import selectinload

            from app.db.tables import User as UserTable

            result = await session.execute(
                select(UserTable)
                .options(selectinload(UserTable.subscription))
                .where(UserTable.id == user.id)
            )
            user_db = result.scalar_one()
            await auth_redis.setex(
                f"auth-session-id:{token}",
                test_settings.auth_session_expire_seconds,
                AuthSessionSchema(
                    id=user_db.id,
                    email=user_db.email,
                    nickname=user_db.nickname,
                    subscription=Subscription.model_validate(user_db.subscription),
                    time_created=user_db.time_created,
                    time_updated=user_db.time_updated,
                    is_artist=user_db.is_artist,
                    is_active=user_db.is_active,
                    is_superuser=user_db.is_superuser,
                    is_verified=user_db.is_verified,
                ).model_dump_json(),
            )
            client.cookies.set("satk", token)
        return client

    return _make_client


@pytest.fixture
async def authorized_client(
    make_authorized_client,
    test_user,
    test_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    client = await make_authorized_client(test_user, test_session, token="SESSIONTOKEN")
    yield client


@pytest.fixture
async def authorized_client_artist(
    make_authorized_client,
    test_artist,
    test_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    client = await make_authorized_client(
        test_artist, test_session, token="SESSIONTOKEN_ARTIST"
    )
    yield client


@pytest.fixture
async def authorized_client_admin(
    make_authorized_client,
    test_admin,
    test_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    client = await make_authorized_client(
        test_admin, test_session, token="SESSIONTOKEN_ADMIN"
    )
    yield client
