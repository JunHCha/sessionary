from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.auth import view as auth_view
from app.auth.access import current_user_placeholder
from app.containers.application import ApplicationContainer
from app.core.errors.http_error import http_error_handler
from app.core.errors.validation_error import http400_error_handler
from app.core.middlewares import AuthSessionMiddleware
from app.lecture import view as lecture_view
from app.lesson import view as lesson_view
from app.ping import view as ping_view
from app.ticket import view as ticket_view
from app.user import view as user_view


def create_container() -> ApplicationContainer:
    container = ApplicationContainer()
    container.wire(
        modules=[
            "app.user.view",
            "app.lecture.view",
            "app.lesson.view",
            "app.ticket.view",
            "app.containers.auth",
            "app.auth.access",
        ]
    )
    return container


def get_application(container: ApplicationContainer | None = None) -> FastAPI:
    if container is None:
        container = create_container()

    settings = container.settings()
    settings.configure_logging()

    auth_backend = container.auth.auth_backend()

    application = FastAPI(**settings.fastapi_kwargs)
    application.container = container
    application.dependency_overrides[current_user_placeholder] = (
        auth_backend.components.current_user()
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(
        AuthSessionMiddleware, settings=settings, auth_backend=auth_backend
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http400_error_handler)

    api_router = APIRouter()
    api_router.include_router(user_view.app_router, prefix="/user", tags=["user"])
    api_router.include_router(
        auth_view.create_auth_router(auth_backend), prefix="/user", tags=["auth"]
    )
    api_router.include_router(
        lecture_view.app_router, prefix="/lecture", tags=["lecture"]
    )
    api_router.include_router(lesson_view.app_router, prefix="/lesson", tags=["lesson"])
    api_router.include_router(ticket_view.app_router, prefix="/ticket", tags=["ticket"])
    api_router.include_router(ping_view.app_router, prefix="/ping", tags=["ping"])
    application.include_router(api_router)

    return application


def create_app() -> FastAPI:
    return get_application()


app: FastAPI | None = None


def get_app() -> FastAPI:
    global app
    if app is None:
        app = create_app()
    return app
