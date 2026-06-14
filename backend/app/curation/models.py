from app.core.models import BaseSchema
from app.lecture.models import LectureInList


class SetCurationBody(BaseSchema):
    lecture_ids: list[int]


class CurationData(BaseSchema):
    TRENDING: list[LectureInList]
    NEW: list[LectureInList]


class GetCurationSchema(BaseSchema):
    data: CurationData
