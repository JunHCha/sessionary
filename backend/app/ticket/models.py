import datetime
from typing import Literal

from app.core.models import BaseModel


class LectureAccessStatus(BaseModel):
    accessible: bool
    reason: (
        Literal["unlimited", "ticket_used", "no_ticket", "ticket_expired"] | None
    ) = None
    expires_at: datetime.datetime | None = None
    ticket_count: int
