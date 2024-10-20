from __future__ import annotations

import datetime
import uuid
from typing import List

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class Lecture(Base):
    id: int
    title: str
    artist: ArtistInfo | None
    lessons: List[LessonInLecture]
    description: str
    length_sec: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class ArtistInfo(Base):
    id: uuid.UUID
    nickname: str
    is_artist: bool


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


class LectureForArtistView(Base):
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
    owner: ArtistInfo
    lessons: list[LessonInLecture]
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
