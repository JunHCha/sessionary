from pydantic import BaseModel

from app.models import Lecture, LectureInFetch, PaginationMeta


class FetchRecommendedLecuturesSchema(BaseModel):
    data: list[LectureInFetch]
    meta: PaginationMeta


class GetLectureSchema(BaseModel):
    data: Lecture
