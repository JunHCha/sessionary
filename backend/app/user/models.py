from __future__ import annotations

import datetime
import uuid

from fastapi_users import schemas

from app.core.models import Base
from app.lecture.models import LectureForArtistView
from app.subscription.models import Subscription


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


class GetArtistsResponse(Base):
    data: list[UserArtistInfo]
