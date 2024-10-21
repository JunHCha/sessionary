from __future__ import annotations

import datetime
import uuid
from typing import List

from app.core.models import BaseModel, BaseSchema
from app.lesson.models import LessonInLecture


class LectureDetail(BaseModel):
    id: int
    title: str
    artist: ArtistInfoInLecture | None
    lessons: List[LessonInLecture]
    description: str
    length_sec: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class ArtistInfoInLecture(BaseModel):
    id: uuid.UUID
    nickname: str
    is_artist: bool


class LectureList(BaseModel):
    id: int
    title: str
    description: str
    length_sec: int
    lecture_count: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class Playlist(BaseModel):
    id: int
    title: str
    owner: ArtistInfoInLecture
    lessons: list[LessonInLecture]
    time_created: datetime.datetime
    time_updated: datetime.datetime


class PaginationMeta(BaseModel):
    total_items: int
    total_pages: int
    curr_page: int
    per_page: int


class FetchRecommendedLecuturesSchema(BaseSchema):
    data: list[LectureList]
    meta: PaginationMeta


class GetLectureSchema(BaseSchema):
    data: LectureDetail


class CreateLectureBody(BaseSchema):
    title: str
    description: str = "새로운 강의"


class CreateLectureResponseSchema(GetLectureSchema):
    pass
