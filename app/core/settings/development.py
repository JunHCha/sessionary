import logging

from app.core.settings.base import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev Session Away Backend Server"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env.dev"
