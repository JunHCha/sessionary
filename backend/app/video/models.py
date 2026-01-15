import datetime
from typing import Literal

from app.core.models import BaseModel


class VideoURLResponse(BaseModel):
    url: str
    type: Literal["hls", "direct"]
    expires_at: datetime.datetime
