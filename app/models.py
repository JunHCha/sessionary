import datetime
import uuid
from typing import Literal

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserRead(schemas.BaseUser[uuid.UUID]):
    nickname: str
    email: str
    is_artist: bool
    is_superuser: bool


class UserUpdate(schemas.BaseUserUpdate):
    nickname: str


class UserReadPublic(Base):
    nickname: str
    is_artist: bool


class GetArtistsResponse(Base):
    data: list["UserArtistInfo"]


class LectureForArtistView(Base):
    id: int
    title: str
    description: str
    length_sec: int
    lecture_count: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class UserArtistInfo(Base):
    id: uuid.UUID
    nickname: str
    time_created: datetime.datetime
    lectures: list[LectureForArtistView]


class AuthSessionSchema(Base):
    id: uuid.UUID
    email: str
    nickname: str
    is_artist: bool
    subscription: "Subscription"
    time_created: datetime.datetime | None
    time_updated: datetime.datetime | None
    is_active: bool
    is_superuser: bool
    is_verified: bool


class Subscription(Base):
    id: uuid.UUID
    name: Literal["ticket", "experimental", "personal", "group"]
    is_active: bool
    ticket_count: int
    expires_at: datetime.datetime
    time_created: datetime.datetime


class Lecture(Base):
    id: int
    title: str
    artists: list[UserArtistInfo]
    description: str
    length_sec: int
    lecture_count: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class Playlist(Base):
    id: int
    title: str
    owner: UserRead
    lessons: list["Lesson"]
    time_created: datetime.datetime
    time_updated: datetime.datetime


class Lesson(Base):
    id: int
    title: str
    artist_id: uuid.UUID
    lecture: Lecture
    artist: UserArtistInfo
    sheetmusic_url: str
    video_url: str
    text: str
    time_created: datetime.datetime
    time_updated: datetime.datetime