from dependency_injector import containers, providers

from app.lecture.repository import LectureRepository
from app.lecture.service import LectureService
from app.user.repository import UserRepository
from app.user.service import UserService


class ServicesContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    database = providers.DependenciesContainer()

    user_repository = providers.Factory(
        UserRepository,
        session_manager=database.session_manager,
    )

    lecture_repository = providers.Factory(
        LectureRepository,
        session_manager=database.session_manager,
    )

    user_service = providers.Factory(
        UserService,
        repository=user_repository,
    )

    lecture_service = providers.Factory(
        LectureService,
        repository=lecture_repository,
    )
