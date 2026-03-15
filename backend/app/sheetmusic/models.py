import datetime

from app.core.models import BaseModel


class SheetmusicURLResponse(BaseModel):
    url: str
    expires_at: datetime.datetime
