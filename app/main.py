from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.core.errors.http_error import http_error_handler
from app.core.errors.validation_error import http400_error_handler
from app.core.settings import get_app_settings
from app.ping import api as ping_api
from app.user import api as user_api


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http400_error_handler)

    api_router = APIRouter()
    api_router.include_router(user_api.app_router, prefix="/user", tags=["user"])
    api_router.include_router(ping_api.app_router, prefix="/ping", tags=["ping"])
    application.include_router(api_router)

    return application


app = get_application()
