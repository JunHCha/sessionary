import asyncio
from os import environ
from typing import AsyncGenerator, Iterator

import pytest
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
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
async def auth_redis() -> AsyncGenerator[Redis, None]:
    settings = get_app_settings()
    auth_redis = Redis.from_url(
        settings.auth_redis_url, decode_responses=True, socket_timeout=1
    )
    yield auth_redis
    await auth_redis.flushdb()


@pytest.fixture
async def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def user_manager_stub(app, test_session: AsyncSession):

    from fastapi_users import exceptions
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

    from app.core.auth.dependancy import get_user_manager
    from app.core.auth.manager import UserManager
    from app.db.dependency import get_user_db
    from app.db.tables import User

    class StubUserManager(UserManager):
        async def authenticate(
            self, credentials: OAuth2PasswordRequestForm
        ) -> User | None:
            try:
                user = await self.get_by_email(credentials.username)
            except exceptions.UserNotExists:
                return None
            return user

    async def get_test_user_manager(user_db=Depends(get_user_db)):
        yield StubUserManager(user_db=user_db)

    app.dependency_overrides[get_user_manager] = get_test_user_manager

    test_user_db = SQLAlchemyUserDatabase(test_session, User, None)
    return StubUserManager(user_db=test_user_db)
