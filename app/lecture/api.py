import uuid

from fastapi import APIRouter, Depends, Query

from app.depends.service import get_lecture_service
from app.lecture.schemas import GetRecommendedLecuturesSchema
from app.lecture.service import BaseLectureService

app_router = APIRouter()


@app_router.get("", response_model=GetRecommendedLecuturesSchema)
async def get_lectures(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=10),
    lecture_svc: BaseLectureService = Depends(get_lecture_service),
):
    lectures, meta = await lecture_svc.get_recommended(page, per_page)
    return GetRecommendedLecuturesSchema(data=lectures, meta=meta)


@app_router.get("/{id}")
async def get_lecture(
    id: uuid.UUID, lecture_svc: BaseLectureService = Depends(get_lecture_service)
):
    result = await lecture_svc.get_lecture_detail(id)
    return result
