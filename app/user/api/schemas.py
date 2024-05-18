import uuid

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict

from app.models import UserArtistInfo


class UserRead(schemas.BaseUser[uuid.UUID]):
    nickname: str
    email: str
    is_artist: bool
    is_superuser: bool


class UserUpdate(schemas.BaseUserUpdate):
    nickname: str


class UserReadPublic(BaseModel):
    nickname: str
    is_artist: bool

    model_config = ConfigDict(from_attributes=True)


class GetArtistsResponse(BaseModel):
    data: list[UserArtistInfo]
