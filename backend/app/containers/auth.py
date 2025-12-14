from typing import AsyncGenerator

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.backend import AuthBackend
from app.auth.manager import UserManager
from app.db.tables import OAuthAccount, User


async def get_user_db(
    session: AsyncSession = Depends(Provide["database.session"]),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


class AuthContainer(containers.DeclarativeContainer):
    settings = providers.Dependency()
    database = providers.DependenciesContainer()

    auth_backend = providers.Singleton(
        AuthBackend,
        settings=settings,
        get_user_manager=get_user_manager,
    )
