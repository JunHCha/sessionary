from typing import AsyncGenerator

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings.base import AppEnv, AppSettings, BaseAppSettings
from app.core.settings.development import DevAppSettings
from app.core.settings.staging import StagingAppSettings
from app.core.settings.test import TestAppSettings
from app.db.session import SessionManager


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


async def get_session(
    session_manager: SessionManager,
) -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.async_session() as session:
        yield session


class DatabaseContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    settings = providers.Singleton(get_settings_class())

    session_manager = providers.Singleton(
        SessionManager,
        settings=settings,
    )

    session = providers.Resource(
        get_session,
        session_manager=session_manager,
    )
