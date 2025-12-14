from fastapi import APIRouter

from app.auth.backend import AuthBackend


def create_auth_router(auth_backend: AuthBackend) -> APIRouter:
    router = APIRouter()
    router.include_router(auth_backend.authenticate_router, prefix="/auth")
    router.include_router(auth_backend.password_reset_router, prefix="/auth")
    router.include_router(auth_backend.oauth_router, prefix="/oauth/google")
    router.include_router(auth_backend.users_router)
    return router
