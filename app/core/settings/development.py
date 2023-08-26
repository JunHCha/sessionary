import logging

from app.core.settings.base import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev Session Away Backend Server"

    logging_level: int = logging.DEBUG

    model_config = AppSettings.model_config.update({"env_file": ".env.dev"})
