from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.auth.access import superuser
from app.containers.application import ApplicationContainer
from app.curation.models import GetCurationSchema, SetCurationBody
from app.curation.service import CurationService
from app.db.tables import CurationSection

app_router = APIRouter()


@app_router.get("", response_model=GetCurationSchema)
@inject
async def get_curation(
    curation_service: CurationService = Depends(
        Provide[ApplicationContainer.services.curation_service]
    ),
):
    data = await curation_service.get_curation()
    return GetCurationSchema(data=data)


@app_router.put("/{section}")
@inject
async def set_curation(
    section: CurationSection,
    body: SetCurationBody,
    user=Depends(superuser),
    curation_service: CurationService = Depends(
        Provide[ApplicationContainer.services.curation_service]
    ),
):
    await curation_service.set_section(section, body.lecture_ids)
    return {"ok": True}
