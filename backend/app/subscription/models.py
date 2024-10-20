from __future__ import annotations

import datetime
import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class Subscription(Base):
    id: uuid.UUID
    name: Literal["ticket", "experimental", "personal", "group"]
    is_active: bool
    ticket_count: int
    expires_at: datetime.datetime
    time_created: datetime.datetime
