from os import environ
from pathlib import Path
from typing import AsyncGenerator

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import exceptions
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.manager import UserManager
from app.auth.strategy import RedisMock
from app.containers.application import ApplicationContainer
from app.core.settings.test import TestAppSettings
from app.db import tables
from tests.containers import TestDatabaseContainer, TestSessionManager


@pytest.fixture(scope="session")
def setup_env():
    environ["APP_ENV"] = "test"
    yield


def _delete_test_db():
    test_db_paths = [
        Path("test.db"),
        Path("backend/test.db"),
        Path(__file__).parent.parent / "test.db",
    ]
    for db_path in test_db_paths:
        if db_path.exists():
            db_path.unlink()


@pytest.fixture(scope="session")
def test_container(setup_env) -> ApplicationContainer:
    container = ApplicationContainer()
    container.settings.override(TestAppSettings())
    container.database.override(TestDatabaseContainer(settings=container.settings))
    container.wire(
        modules=[
            "app.user.view",
            "app.lecture.view",
            "app.containers.auth",
            "app.auth.access",
        ]
    )
    yield container
    container.database.session_manager.reset()
    container.unwire()
    _delete_test_db()


@pytest.fixture(scope="session")
def test_settings(test_container: ApplicationContainer) -> TestAppSettings:
    return test_container.settings()


@pytest.fixture(scope="session")
def stub_sess_manager(
    test_container: ApplicationContainer,
) -> TestSessionManager:
    return test_container.database.session_manager()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database(stub_sess_manager: TestSessionManager):
    engine = stub_sess_manager.engine
    async with engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.drop_all)


@pytest.fixture(autouse=True)
async def migrate_table_schemas(stub_sess_manager: TestSessionManager):
    async with stub_sess_manager.engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.create_all)

    yield

    async with stub_sess_manager.engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.drop_all)


@pytest.fixture
async def test_session(
    stub_sess_manager: TestSessionManager,
) -> AsyncGenerator[AsyncSession, None]:
    async with stub_sess_manager.async_session() as session:
        yield session


@pytest.fixture
async def auth_redis() -> AsyncGenerator[RedisMock, None]:
    redis_mock = RedisMock()
    yield redis_mock
    await redis_mock.flushdb()


@pytest.fixture
async def app(
    test_container: ApplicationContainer, stub_sess_manager: TestSessionManager
) -> FastAPI:
    from app.main import get_application

    application = get_application(container=test_container)
    return application


@pytest.fixture
async def user_manager_stub(
    app: FastAPI,
    test_session: AsyncSession,
    test_container: ApplicationContainer,
):
    from app.containers.auth import get_user_db, get_user_manager

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
