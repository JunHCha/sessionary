from __future__ import annotations

import datetime
import uuid
from typing import Literal

from app.core.models import BaseModel


class Subscription(BaseModel):
    id: uuid.UUID
    name: Literal["ticket", "experimental", "personal", "group"]
    is_active: bool
    time_created: datetime.datetime
