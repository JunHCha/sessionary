import datetime
import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict


class Subscription(BaseModel):
    id: uuid.UUID
    name: Literal["ticket", "experimental", "personal", "group"]
    is_active: bool
    ticket_count: int
    expires_at: datetime.datetime
    time_created: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
