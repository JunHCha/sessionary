from dependency_injector import containers, providers

from app.containers.auth import AuthContainer
from app.containers.database import DatabaseContainer
from app.containers.services import ServicesContainer
from app.core.settings.base import AppEnv, AppSettings, BaseAppSettings
from app.core.settings.development import DevAppSettings
from app.core.settings.staging import StagingAppSettings
from app.core.settings.test import TestAppSettings


def get_settings_class() -> type[AppSettings]:
    """
    현재 실행 환경에 대응하는 AppSettings 하위 클래스를 선택한다.
    
    환경 설정(BaseAppSettings().app_env)에 따라 적절한 설정 클래스(TestAppSettings, DevAppSettings, StagingAppSettings 또는 AppSettings)를 반환한다.
    
    Returns:
        type[AppSettings]: 선택된 AppSettings 하위 클래스 타입.
    """
    environments = {
        AppEnv.test: TestAppSettings,
        AppEnv.dev: DevAppSettings,
        AppEnv.staging: StagingAppSettings,
        AppEnv.prod: AppSettings,
    }
    app_env = BaseAppSettings().app_env
    config = environments[app_env]

    return config


def get_app_settings() -> AppSettings:
    return get_settings_class()()


class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.user.view",
            "app.lecture.view",
            "app.containers.auth",
            "app.auth.access",
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

    auth = providers.Container(
        AuthContainer,
        settings=settings,
        database=database,
    )