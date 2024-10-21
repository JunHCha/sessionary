import datetime

from app.core.models import BaseModel


class LessonInLecture(BaseModel):
    id: int
    title: str
    length_sec: int
    lecture_ordering: int
    time_created: datetime.datetime
    time_updated: datetime.datetime
