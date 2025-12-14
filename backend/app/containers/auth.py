from typing import AsyncGenerator

from dependency_injector import containers, providers
from fastapi import Depends, Request
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.auth.backend import AuthBackend
from app.auth.manager import UserManager
from app.db.tables import OAuthAccount, User


async def get_user_db(request: Request) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    session_manager = request.app.container.database.session_manager()
    async with session_manager.async_session() as session:
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
