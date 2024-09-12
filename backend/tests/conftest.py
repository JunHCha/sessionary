import asyncio
from os import environ
from typing import AsyncGenerator

import pytest
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import exceptions
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.core.auth.manager import UserManager
from app.core.settings.base import AppSettings
from app.db import tables
from app.db.session import SessionManager
from app.depends.auth import get_user_db, get_user_manager
from app.depends.db import get_session
from app.depends.settings import get_app_settings
from tests.mock.redis_mock import RedisMock


@pytest.fixture(scope="session")
def setup_env():
    environ["APP_ENV"] = "test"

    yield


@pytest.fixture(scope="session")
def stub_sess_manager(setup_env) -> SessionManager:
    settings = get_app_settings()

    class TestSessionManager(SessionManager):
        def __init__(self, settings: AppSettings):
            self._engine = create_async_engine(
                settings.database_url,
                echo=True,
            )
            self._async_session_factory = async_scoped_session(
                async_sessionmaker(
                    self._engine,
                    expire_on_commit=False,
                    autoflush=False,
                ),
                scopefunc=asyncio.current_task,
            )

    return TestSessionManager(settings)


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database(stub_sess_manager):
    engine = stub_sess_manager.engine
    async with engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.drop_all)


@pytest.fixture(autouse=True)
async def migrate_table_schemas(stub_sess_manager: SessionManager):

    async with stub_sess_manager.engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.create_all)

    yield

    async with stub_sess_manager.engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.drop_all)


@pytest.fixture
async def test_session(stub_sess_manager) -> AsyncGenerator[AsyncSession, None]:
    async with stub_sess_manager.async_session() as session:
        yield session


@pytest.fixture
async def auth_redis() -> AsyncGenerator[RedisMock, None]:
    redis_mock = RedisMock()
    yield redis_mock
    await redis_mock.flushdb()


@pytest.fixture
async def app(stub_sess_manager) -> FastAPI:
    from app.main import get_application

    async def override_get_session():
        async with stub_sess_manager.async_session() as session:
            yield session

    app = get_application()
    app.dependency_overrides[get_session] = override_get_session
    return app


@pytest.fixture
async def user_manager_stub(app, test_session: AsyncSession):

    class StubUserManager(UserManager):
        async def authenticate(
            self, credentials: OAuth2PasswordRequestForm
        ) -> tables.User | None:
            try:
                user = await self.get_by_email(credentials.username)
            except exceptions.UserNotExists:
                return None
            return user

    async def get_test_user_manager(user_db=Depends(get_user_db)):
        yield StubUserManager(user_db=user_db)

    app.dependency_overrides[get_user_manager] = get_test_user_manager

    test_user_db = SQLAlchemyUserDatabase(test_session, tables.User, None)
    return StubUserManager(user_db=test_user_db)
