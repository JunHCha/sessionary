import datetime
import uuid

from pydantic import BaseModel


class UserArtistInfo(BaseModel):
    id: uuid.UUID
    nickname: str
    time_created: datetime.datetime
    lectures: list[str]
