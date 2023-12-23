from os import environ
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core.settings import get_app_settings
from app.db.session import SessionManager


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    environ["APP_ENV"] = "test"
    environ[
        "DATABASE_URL"
    ] = "postgresql+asyncpg://user:password@127.0.0.1:5433/sessionaway"
    environ["AUTH_REDIS_URL"] = "redis://localhost:6379/4"
    yield


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    from app.db.tables import Base

    sync_engine = create_engine(
        get_app_settings()
        .database_url.unicode_string()
        .replace("postgresql+asyncpg://", "postgresql://")
    )

    if database_exists(sync_engine.url):
        drop_database(sync_engine.url)

    create_database(sync_engine.url)
    Base.metadata.create_all(sync_engine)

    yield

    sync_engine.dispose()


@pytest.fixture
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    settings = get_app_settings()
    session_manager = SessionManager(settings)
    async with session_manager.async_session() as session:
        yield session


@pytest.fixture
async def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
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
async def authorized_client(client: AsyncClient, test_user) -> AsyncClient:
    auth_redis = Redis.from_url(
        get_app_settings().auth_redis_url, decode_responses=True, socket_timeout=1
    )
    await auth_redis.set("auth-session-id:SESSIONTOKEN", str(test_user.id))
    client.cookies = {get_app_settings().cookie_name: "SESSIONTOKEN"}
    yield client
    await auth_redis.flushdb()


@pytest.fixture(autouse=True)
async def teardown(test_session: AsyncSession):
    yield

    from app.db.tables import Base

    for table in reversed(Base.metadata.sorted_tables):
        await test_session.execute(table.delete())
    await test_session.commit()
