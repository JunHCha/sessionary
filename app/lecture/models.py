import datetime

from pydantic import BaseModel

from app.user.models import UserArtistInfo


class Lecture(BaseModel):
    id: int
    title: str
    artists: list[UserArtistInfo]
    description: str
    length_sec: int
    lecture_count: int
    time_created: datetime.datetime
    time_updated: datetime.datetime
