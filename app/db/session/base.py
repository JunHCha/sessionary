from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())
