from dependency_injector import containers, providers

from app.containers.database import DatabaseContainer
from app.containers.services import ServicesContainer


class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.user.api",
            "app.lecture.api",
        ]
    )

    database = providers.Container(DatabaseContainer)

    services = providers.Container(
        ServicesContainer,
        database=database,
    )
