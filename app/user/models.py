import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class LectureForArtistView(BaseModel):
    id: int
    title: str
    description: str
    length_sec: int
    lecture_count: int
    time_created: datetime.datetime
    time_updated: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class UserArtistInfo(BaseModel):
    id: uuid.UUID
    nickname: str
    time_created: datetime.datetime
    lectures: list[LectureForArtistView]

    model_config = ConfigDict(from_attributes=True)


class AuthSessionSchema(BaseModel):
    id: uuid.UUID
    email: str
    nickname: str
    is_artist: bool
    subscription_id: int | None
    time_created: datetime.datetime | None
    time_updated: datetime.datetime | None
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)
