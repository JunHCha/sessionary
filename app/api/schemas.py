from pydantic import BaseModel


class UserResponseSchema(BaseModel):
    nickname: str
    email: str
    is_artist: bool
    is_superuser: bool


class UserUpdateSchema(BaseModel):
    nickname: str
