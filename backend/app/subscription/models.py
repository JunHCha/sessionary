from __future__ import annotations

import datetime
import uuid
from typing import Literal

from app.core.models import Base


class Subscription(Base):
    id: uuid.UUID
    name: Literal["ticket", "experimental", "personal", "group"]
    is_active: bool
    ticket_count: int
    expires_at: datetime.datetime
    time_created: datetime.datetime
