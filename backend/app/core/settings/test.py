import logging

from pydantic import SecretStr

from app.core.settings.base import AppSettings


class TestAppSettings(AppSettings):
    # FastAPI kwargs
    debug: bool = True

    # PostgreSQL DB
    database_url: str = "sqlite+aiosqlite:///./test.db"

    max_connection_count: int = 2
    min_connection_count: int = 2

    # Security
    secret_key: SecretStr = SecretStr("test_secret")
    allowed_hosts: list[str] = ["*"]

    # Authentication
    cookie_name: str = "satk"
    auth_session_expire_seconds: int = 60
    auth_session_refresh_interval: int = 2
    auth_redis_url: str = ""

    # Logging
    logging_level: int = logging.DEBUG
    loggers: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
