from fastapi import APIRouter, Depends, Query

from app.depends.service import get_lecture_service
from app.lecture.schemas import FetchRecommendedLecuturesSchema, GetLectureSchema
from app.lecture.service import BaseLectureService

app_router = APIRouter()


@app_router.get("", response_model=FetchRecommendedLecuturesSchema)
async def get_lectures(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=10),
    lecture_svc: BaseLectureService = Depends(get_lecture_service),
):
    lectures, meta = await lecture_svc.get_recommended(page, per_page)
    return FetchRecommendedLecuturesSchema(data=lectures, meta=meta)


@app_router.get("/{lecture_id}", response_model=GetLectureSchema)
async def get_lecture(
    lecture_id: int, lecture_svc: BaseLectureService = Depends(get_lecture_service)
):
    lecture = await lecture_svc.get_lecture_detail(lecture_id)
    return GetLectureSchema(data=lecture)
