from pydantic import BaseModel

from app.lecture.models import Lecture


class GetRecommendedLecuturesSchema(BaseModel):
    data: list[Lecture]
