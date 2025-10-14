from __future__ import annotations

import datetime
import json
import uuid
from typing import List, Literal

from pydantic import field_validator

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


LectureType = Literal["원곡카피", "해석버전", "기본기"]
DifficultyLevel = Literal["Easy", "Intermediate", "Advanced"]
TagsTuple = tuple[LectureType, DifficultyLevel]


class LectureInList(BaseModel):
    id: int
    thumbnail: str | None
    title: str
    artist: str | None
    description: str
    tags: tuple[LectureType, DifficultyLevel] | None
    length_sec: int
    lecture_count: int
    time_created: datetime.datetime
    time_updated: datetime.datetime

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            return tuple(json.loads(value))
        return value


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
    data: list[LectureInList]
    meta: PaginationMeta


class GetLectureSchema(BaseSchema):
    data: LectureDetail


class CreateLectureBody(BaseSchema):
    title: str
    description: str = "새로운 강의"


class CreateLectureResponseSchema(GetLectureSchema):
    pass
