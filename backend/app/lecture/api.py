from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.containers.application import ApplicationContainer
from app.core.auth.access import superuser
from app.lecture.models import (
    CreateLectureBody,
    CreateLectureResponseSchema,
    FetchRecommendedLecuturesSchema,
    GetLectureSchema,
)
from app.lecture.service import BaseLectureService

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
    lecture_svc: BaseLectureService = Depends(
        Provide[ApplicationContainer.services.lecture_service]
    ),
):
    lecture = await lecture_svc.get_lecture_detail(lecture_id)
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

