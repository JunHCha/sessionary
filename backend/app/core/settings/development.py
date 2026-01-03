import logging

from pydantic import ConfigDict

from app.core.settings.base import AppSettings


class DevAppSettings(AppSettings):
    model_config = ConfigDict(env_file=".env.dev", extra="ignore")

    # FastAPI kwargs
    debug: bool = True
    title: str = "Dev Sessionary Backend Server"

    # logging
    logging_level: int = logging.DEBUG
