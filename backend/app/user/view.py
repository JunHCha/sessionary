from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.containers.application import ApplicationContainer
from app.user.models import GetArtistsResponse
from app.user.service import BaseUserService

app_router = APIRouter()


@app_router.get("/artists", response_model=GetArtistsResponse)
@inject
async def get_artists(
    user_svc: BaseUserService = Depends(
        Provide[ApplicationContainer.services.user_service]
    ),
):
    results = await user_svc.get_artists()
    return GetArtistsResponse(data=results)
