from dependency_injector import containers, providers

from app.lecture.repository import LectureRepository
from app.lecture.service import LectureService
from app.lesson.repository import LessonRepository
from app.session.repository import SessionRepository
from app.session.service import SessionService
from app.ticket.repository import TicketRepository
from app.ticket.service import TicketService
from app.user.repository import UserRepository
from app.user.service import UserService
from app.video.service import VideoProvider


def _create_video_provider(settings) -> VideoProvider:
    if settings.video_provider == "mock":
        from app.video.mock import MockVideoProvider

        return MockVideoProvider()
    elif settings.video_provider == "local":
        from app.video.minio import MinIOVideoProvider

        return MinIOVideoProvider(
            endpoint=settings.video_storage_endpoint,
            access_key=settings.video_storage_access_key,
            secret_key=settings.video_storage_secret_key,
            bucket_name=settings.video_storage_bucket_name,
            secure=settings.video_storage_secure,
        )
    elif settings.video_provider == "cloudflare":
        from app.video.cloudflare import CloudflareVideoProvider

        return CloudflareVideoProvider(
            account_id=settings.cloudflare_account_id,
            api_token=settings.cloudflare_api_token,
        )
    else:
        raise ValueError(f"Unknown video provider: {settings.video_provider}")


class ServicesContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    database = providers.DependenciesContainer()
    settings = providers.Dependency()

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

    ticket_repository = providers.Factory(
        TicketRepository,
        session_manager=database.session_manager,
    )

    ticket_service = providers.Factory(
        TicketService,
        repository=ticket_repository,
    )

    lesson_repository = providers.Factory(
        LessonRepository,
        session_manager=database.session_manager,
    )

    video_provider = providers.Factory(
        _create_video_provider,
        settings=settings,
    )

    session_repository = providers.Factory(
        SessionRepository,
        session_manager=database.session_manager,
    )

    session_service = providers.Factory(
        SessionService,
        repository=session_repository,
        video_provider=video_provider,
    )
