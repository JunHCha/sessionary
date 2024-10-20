from __future__ import annotations

import datetime
import uuid
from typing import List

from pydantic import BaseModel

from app.core.models import Base
from app.lesson.models import LessonInLecture


class LectureDetail(Base):
    id: int
    title: str
    artist: ArtistInfoInLecture | None
    lessons: List[LessonInLecture]
    description: str
    length_sec: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class ArtistInfoInLecture(Base):
    id: uuid.UUID
    nickname: str
    is_artist: bool


class LectureList(Base):
    id: int
    title: str
    description: str
    length_sec: int
    lecture_count: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class Playlist(Base):
    id: int
    title: str
    owner: ArtistInfoInLecture
    lessons: list[LessonInLecture]
    time_created: datetime.datetime
    time_updated: datetime.datetime


class PaginationMeta(Base):
    total_items: int
    total_pages: int
    curr_page: int
    per_page: int


class FetchRecommendedLecuturesSchema(BaseModel):
    data: list[LectureList]
    meta: PaginationMeta


class GetLectureSchema(BaseModel):
    data: LectureDetail


class CreateLectureBody(BaseModel):
    title: str
    description: str = "새로운 강의"


class CreateLectureResponseSchema(GetLectureSchema):
    pass
