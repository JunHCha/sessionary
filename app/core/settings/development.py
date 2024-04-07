import logging

from app.core.settings.base import AppSettings


class DevAppSettings(AppSettings):
    # FastAPI kwargs
    debug: bool = True
    title: str = "Dev Session Away Backend Server"

    # logging
    logging_level: int = logging.DEBUG
