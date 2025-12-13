from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.containers.application import ApplicationContainer
from app.core.auth.backend import auth_backend
from app.core.errors.http_error import http_error_handler
from app.core.errors.validation_error import http400_error_handler
from app.core.middlewares import AuthSessionMiddleware
from app.lecture import api as lecture_api
from app.ping import api as ping_api
from app.user import api as user_api


def create_container() -> ApplicationContainer:
    container = ApplicationContainer()
    container.wire(
        modules=[
            "app.user.api",
            "app.lecture.api",
        ]
    )
    return container


def get_application(container: ApplicationContainer | None = None) -> FastAPI:
    if container is None:
        container = create_container()

    settings = container.settings()
    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)
    application.container = container

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
    api_router.include_router(user_api.app_router, prefix="/user", tags=["user"])
    api_router.include_router(
        lecture_api.app_router, prefix="/lecture", tags=["lecture"]
    )
    api_router.include_router(ping_api.app_router, prefix="/ping", tags=["ping"])
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
