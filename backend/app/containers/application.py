from dependency_injector import containers, providers

from app.containers.database import DatabaseContainer
from app.containers.services import ServicesContainer
from app.core.settings.base import AppEnv, AppSettings, BaseAppSettings
from app.core.settings.development import DevAppSettings
from app.core.settings.staging import StagingAppSettings
from app.core.settings.test import TestAppSettings


def get_settings_class() -> type[AppSettings]:
    environments = {
        AppEnv.test: TestAppSettings,
        AppEnv.dev: DevAppSettings,
        AppEnv.staging: StagingAppSettings,
        AppEnv.prod: AppSettings,
    }
    app_env = BaseAppSettings().app_env
    config = environments[app_env]

    if config == DevAppSettings:
        config.model_config.update({"env_file": ".env.dev"})

    return config


class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.user.api",
            "app.lecture.api",
        ]
    )

    settings = providers.Singleton(get_settings_class())

    database = providers.Container(
        DatabaseContainer,
        settings=settings,
    )

    services = providers.Container(
        ServicesContainer,
        database=database,
    )
