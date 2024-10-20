import datetime

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class LessonInLecture(Base):
    id: int
    title: str
    length_sec: int
    lecture_ordering: int
    time_created: datetime.datetime
    time_updated: datetime.datetime
