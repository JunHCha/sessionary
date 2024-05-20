from pydantic import BaseModel

from app.models import Lecture, LectureInFetch, PaginationMeta


class FetchRecommendedLecuturesSchema(BaseModel):
    data: list[LectureInFetch]
    meta: PaginationMeta


class GetLectureSchema(BaseModel):
    data: Lecture


class CreateLectureBody(BaseModel):
    title: str
    description: str = "새로운 강의"


class CreateLectureResponseSchema(GetLectureSchema):
    pass
