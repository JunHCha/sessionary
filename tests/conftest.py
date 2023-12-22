from os import environ

import pytest
from alembic import command as alembic_command
from alembic import config as alembic_config
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core.settings import get_app_settings
from app.core.settings.base import AppSettings


@pytest.fixture(scope="session", autouse=True)
def test_settings():
    environ["APP_ENV"] = "test"
    environ[
        "DATABASE_URL"
    ] = "postgresql+asyncpg://user:password@127.0.0.1:5433/sessionaway"
    return get_app_settings()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(test_settings: AppSettings):
    db_url = str(test_settings.database_url).replace(
        "postgresql+asyncpg://", "postgresql://"
    )
    engine = create_engine(db_url)  # type: ignore

    if database_exists(db_url):
        drop_database(db_url)
    create_database(db_url)

    config = alembic_config.Config()
    config.set_main_option("script_location", "app/db/migrations")
    config.set_main_option("test_mode", "true")
    config.set_main_option("sqlalchemy.url", db_url)
    alembic_command.upgrade(config, "head")

    yield

    engine.dispose()


@pytest.fixture
async def app() -> FastAPI:
    from app.main import get_application

    app = get_application()
    return app


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
