from pydantic import BaseModel

from app.models import LectureInFetch, PaginationMeta


class GetRecommendedLecuturesSchema(BaseModel):
    data: list[LectureInFetch]
    meta: PaginationMeta
