from fastapi import APIRouter, Depends

from app.core.auth.backend import auth_backend
from app.depends.service import get_user_service
from app.user.api.schemas import GetArtistsResponse
from app.user.service import BaseUserService

app_router = APIRouter()


@app_router.get("/artists", response_model=GetArtistsResponse)
async def get_artists(user_svc: BaseUserService = Depends(get_user_service)):
    results = await user_svc.get_artists()
    return GetArtistsResponse(data=results)


app_router.include_router(auth_backend.authenticate_router, prefix="/auth")
app_router.include_router(auth_backend.password_reset_router, prefix="/auth")
app_router.include_router(auth_backend.oauth_router, prefix="/oauth/google")
app_router.include_router(auth_backend.users_router)
