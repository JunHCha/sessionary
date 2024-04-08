import asyncio
from os import environ
from typing import AsyncGenerator, Iterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core.settings import get_app_settings
from app.db.session import SessionManager


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()

    yield loop

    loop.close()


@pytest.fixture(scope="session")
def setup_env():
    environ["APP_ENV"] = "test"

    yield


@pytest.fixture(scope="session")
def stub_sess_manager(setup_env) -> SessionManager:
    settings = get_app_settings()
    return SessionManager(settings)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(stub_sess_manager):

    sync_engine_url = stub_sess_manager.engine.url.set(drivername="postgresql")

    if database_exists(sync_engine_url):
        drop_database(sync_engine_url)

    create_database(sync_engine_url)

    yield

    drop_database(sync_engine_url)


@pytest.fixture(autouse=True)
def migrate_table_schemas(stub_sess_manager: SessionManager):
    from app.db.tables import Base

    sync_engine = create_engine(
        stub_sess_manager.engine.url.set(drivername="postgresql")
    )
    Base.metadata.create_all(bind=sync_engine)

    yield

    Base.metadata.drop_all(bind=sync_engine)
    sync_engine.dispose()


@pytest.fixture
async def test_session(stub_sess_manager) -> AsyncGenerator[AsyncSession, None]:
    async with stub_sess_manager.async_session() as session:
        yield session


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
