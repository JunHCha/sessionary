import logging

from pydantic import SecretStr

from app.core.settings.base import AppSettings


class TestAppSettings(AppSettings):
    # FastAPI kwargs
    debug: bool = True

    # PostgreSQL DB
    database_url: str = "sqlite+aiosqlite:///:memory:"

    max_connection_count: int = 2
    min_connection_count: int = 2

    # Security
    secret_key: SecretStr = SecretStr("test_secret")
    allowed_hosts: list[str] = ["*"]

    # Authentication
    cookie_name: str = "satk"
    auth_session_expire_seconds: int = 3600 * 24 * 7 * 4  # 4 weeks
    auth_redis_url: str = "redis://localhost:6379/4"

    # Logging
    logging_level: int = logging.DEBUG
    loggers: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
