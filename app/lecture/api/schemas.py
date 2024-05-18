from pydantic import BaseModel

from app.models import Lecture


class GetRecommendedLecuturesSchema(BaseModel):
    data: list[Lecture]
