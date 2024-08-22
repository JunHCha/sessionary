from functools import lru_cache
from typing import Dict

from app.core.settings.base import AppEnv, AppSettings, BaseAppSettings
from app.core.settings.development import DevAppSettings
from app.core.settings.staging import StagingAppSettings
from app.core.settings.test import TestAppSettings

environments: Dict[AppEnv, AppSettings] = {
    AppEnv.test: TestAppSettings,
    AppEnv.dev: DevAppSettings,
    AppEnv.staging: StagingAppSettings,
    AppEnv.prod: AppSettings,
}


@lru_cache()
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]

    if config == DevAppSettings:
        config.model_config.update({"env_file": ".env.dev"})

    return config()
