import datetime

from pydantic import BaseModel, ConfigDict

from app.models import UserRead, UserReadPublic


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class Lecture(Base):
    id: int
    title: str
    artist: UserReadPublic | None
    lessons: list["LessonInLecture"]
    description: str
    length_sec: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class LectureInFetch(Base):
    id: int
    title: str
    description: str
    length_sec: int
    lecture_count: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class LessonInLecture(Base):
    id: int
    title: str
    length_sec: int
    lecture_ordering: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class Playlist(Base):
    id: int
    title: str
    owner: UserRead
    lessons: list["LessonInLecture"]
    time_created: datetime.datetime
    time_updated: datetime.datetime


class PaginationMeta(Base):
    total_items: int
    total_pages: int
    curr_page: int
    per_page: int


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
