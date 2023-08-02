import logging
import sys
from enum import Enum
from typing import Any, Dict, List, Tuple

from loguru import logger
from pydantic import BaseSettings, PostgresDsn, SecretStr, validator

from app.core.logging import InterceptHandler


class AppEnv(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnv = AppEnv.prod

    class Config:
        env_file = ".env"


class AppSettings(BaseAppSettings):
    # FastAPI kwargs
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Session Away Backend Server"
    version: str = "0.0.0"

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    # PostgreSQL DB
    postgres_server: str | None
    postgres_user: str | None
    postgres_password: str | None
    postgres_db: str | None
    database_url: PostgresDsn | None
    max_connection_count: int = 10
    min_connection_count: int = 10

    @validator("database_url", pre=True)
    def assemble_db_connection(cls, v: str | None, values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        if not (
            values.get("postgres_server")
            and values.get("postgres_db")
            and values.get("postgres_user")
            and values.get("postgres_password")
        ):
            raise ValueError(
                "Either Database URL OR PostgreSQL credentials must be set"
            )
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("postgres_user"),
            password=values.get("postgres_password"),
            host=values.get("postgres_server"),
            path=f"/{values.get('postgres_db') or ''}",
        )

    # Security
    secret_key: SecretStr
    api_prefix: str = "/api"
    jwt_token_prefix: str = "Token"
    allowed_hosts: List[str] = ["*"]
    auth_session_expire_seconds: int = 3600 * 24 * 7 * 4  # 4 weeks

    # OAuth2
    google_client_id: str
    google_client_secret: str

    # Logging
    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])

    class Config:
        validate_assignment = True
