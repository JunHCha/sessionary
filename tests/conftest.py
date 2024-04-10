import asyncio
from os import environ
from typing import AsyncGenerator, Iterator

import pytest
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
