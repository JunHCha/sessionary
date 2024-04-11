import uuid

from fastapi import APIRouter, Depends, Query

from app.lecture.api.schemas import GetRecommendedLecuturesSchema
from app.lecture.service import BaseLectureService, get_lecture_service

app_router = APIRouter()


@app_router.get("", response_model=GetRecommendedLecuturesSchema)
async def get_lectures(
    artist_id: uuid.UUID | None = Query(None),
    lecture_svc: BaseLectureService = Depends(get_lecture_service),
):
    results = await lecture_svc.get_recommended(artist_id=artist_id)
    return GetRecommendedLecuturesSchema(data=results)
