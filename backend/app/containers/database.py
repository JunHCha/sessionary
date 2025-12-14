from dependency_injector import containers, providers

from app.db.session import SessionManager


class DatabaseContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    settings = providers.Dependency()

    session_manager = providers.Singleton(
        SessionManager,
        settings=settings,
    )
