import uuid

from fastapi import APIRouter, Depends, Query

from app.depends.service import get_lecture_service
from app.lecture.api.schemas import GetRecommendedLecuturesSchema
from app.lecture.service import BaseLectureService

app_router = APIRouter()


@app_router.get("", response_model=GetRecommendedLecuturesSchema)
async def get_lectures(
    artist_id: uuid.UUID | None = Query(None),
    lecture_svc: BaseLectureService = Depends(get_lecture_service),
):
    results = await lecture_svc.get_recommended(artist_id=artist_id)
    return GetRecommendedLecuturesSchema(data=results)


@app_router.get("/{id}")
async def get_lecture(
    id: uuid.UUID, lecture_svc: BaseLectureService = Depends(get_lecture_service)
):
    result = await lecture_svc.get_lecture_detail(id)
    return result
