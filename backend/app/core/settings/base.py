import json
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
    staging: str = "staging"
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
    allowed_hosts_str: str = "*"

    @property
    def allowed_hosts(self) -> List[str]:
        """Parse allowed_hosts from JSON array or comma-separated string."""
        v = self.allowed_hosts_str
        # Try JSON first
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass
        # Fall back to comma-separated
        return [host.strip() for host in v.split(",") if host.strip()]

    # Authentication
    cookie_name: str
    cookie_domain: str
    auth_session_expire_seconds: int = 3600 * 24 * 7 * 4  # 4 weeks
    auth_session_refresh_interval: int = 3600 * 24  # 1 day
    auth_redis_url: str

    # OAuth2
    google_client_id: str = "GOOGLE_CLIENT_ID"
    google_client_secret: str = "GOOGLE_CLIENT_SECRET"
    google_oauth_redirect_uri: str = ""

    # Video
    video_provider: str = "local"
    video_storage_endpoint: str = "localhost:9000"
    video_storage_access_key: str = "minioadmin"
    video_storage_secret_key: str = "minioadmin"
    video_storage_bucket_name: str = "videos"
    video_storage_secure: bool = False
    cloudflare_account_id: str = ""
    cloudflare_api_token: str = ""

    # Logging
    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
