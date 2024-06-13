import logging
import sys
from enum import Enum
from typing import Any, Dict, List, Tuple

from loguru import logger
from pydantic import ConfigDict, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings

from app.core.logging import InterceptHandler


class AppEnv(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnv = AppEnv.prod

    model_config = ConfigDict(extra="ignore")


class AppSettings(BaseAppSettings):
    # FastAPI kwargs
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Sessionary Backend Server"
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
    database_url: PostgresDsn
    max_connection_count: int = 10
    min_connection_count: int = 10

    # Security
    secret_key: SecretStr
    allowed_hosts: List[str] = ["*"]

    # Authentication
    cookie_name: str
    auth_session_expire_seconds: int = 3600 * 24 * 7 * 4  # 4 weeks
    auth_redis_url: str

    # OAuth2
    google_client_id: str = "GOOGLE_CLIENT_ID"
    google_client_secret: str = "GOOGLE_CLIENT_SECRET"
    google_oauth_redirect_url: str = ""

    # Logging
    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
