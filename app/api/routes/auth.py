from fastapi import APIRouter

from app.core.auth.backend import auth_backend, fastapi_users, google_oauth_client

router = APIRouter()


router.include_router(fastapi_users.get_auth_router(auth_backend), tags=["auth"])
router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        state_secret="SECRET",  # TODO: 정확한 사용법을 확인 후 수정
        associate_by_email=True,
    ),
    prefix="/oauth/google",
    tags=["auth"],
)
