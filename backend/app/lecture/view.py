from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.auth.access import optional_current_user_placeholder, superuser
from app.containers.application import ApplicationContainer
from app.db.tables import User
from app.lecture.models import (
    CreateLectureBody,
    CreateLectureResponseSchema,
    FetchRecommendedLecuturesSchema,
    GetLectureSchema,
    UpdateLectureBody,
)
from app.lecture.service import BaseLectureService
from app.progress.service import ProgressService

app_router = APIRouter()


@app_router.get("", response_model=FetchRecommendedLecuturesSchema)
@inject
async def get_lectures(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=10),
    lecture_svc: BaseLectureService = Depends(
        Provide[ApplicationContainer.services.lecture_service]
    ),
):
    lectures, meta = await lecture_svc.get_recommended(page, per_page)
    return FetchRecommendedLecuturesSchema(data=lectures, meta=meta)


@app_router.get("/{lecture_id}", response_model=GetLectureSchema)
@inject
async def get_lecture(
    lecture_id: int,
    user: User | None = Depends(optional_current_user_placeholder),
    lecture_svc: BaseLectureService = Depends(
        Provide[ApplicationContainer.services.lecture_service]
    ),
    progress_service: ProgressService = Depends(
        Provide[ApplicationContainer.services.progress_service]
    ),
):
    lecture = await lecture_svc.get_lecture_detail(lecture_id)
    if user is not None:
        progress = await progress_service.get_lecture_progress(user.id, lecture)
        lecture = lecture.model_copy(update={"progress": progress})
    return GetLectureSchema(data=lecture)


@app_router.post("", response_model=CreateLectureResponseSchema, status_code=201)
@inject
async def create_lecture(
    body: CreateLectureBody,
    lecture_svc: BaseLectureService = Depends(
        Provide[ApplicationContainer.services.lecture_service]
    ),
    user=Depends(superuser),
):
    lecture = await lecture_svc.create_lecture(body.title, body.description)
    return GetLectureSchema(data=lecture)


@app_router.patch("/{lecture_id}", response_model=GetLectureSchema)
@inject
async def update_lecture(
    lecture_id: int,
    body: UpdateLectureBody,
    lecture_svc: BaseLectureService = Depends(
        Provide[ApplicationContainer.services.lecture_service]
    ),
    user=Depends(superuser),
):
    fields = body.model_dump(exclude_unset=True)
    lecture = await lecture_svc.update_lecture(lecture_id, fields)
    return GetLectureSchema(data=lecture)
