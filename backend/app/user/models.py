from __future__ import annotations

import datetime
import uuid
from typing import Literal

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict

from app.lecture.models import LectureForArtistView


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


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


class UserArtistInfo(Base):
    id: uuid.UUID
    nickname: str
    time_created: datetime.datetime
    lectures: list[LectureForArtistView]


class Subscription(Base):
    id: uuid.UUID
    name: Literal["ticket", "experimental", "personal", "group"]
    is_active: bool
    ticket_count: int
    expires_at: datetime.datetime
    time_created: datetime.datetime


class AuthSessionSchema(Base):
    id: uuid.UUID
    email: str
    nickname: str
    is_artist: bool
    subscription: Subscription
    time_created: datetime.datetime | None
    time_updated: datetime.datetime | None
    is_active: bool
    is_superuser: bool
    is_verified: bool


class GetArtistsResponse(BaseModel):
    data: list[UserArtistInfo]
