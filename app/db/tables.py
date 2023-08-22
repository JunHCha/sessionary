import random
import string
from typing import List

from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, relationship

from app.db.session.base import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


def random_nickname():
    return "".join(random.choices(string.ascii_lowercase, k=5))


class User(SQLAlchemyBaseUserTableUUID, Base):
    nickname: str = Column(String, default=random_nickname, unique=True, nullable=False)
    is_artist: bool = Column(Boolean, default=False, nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscription.id"), nullable=True)
    # TODO: 자동구독 작업후 nullable False로 바꾸기

    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    # for orm
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    subscription: Mapped["Subscription"] = relationship("Subscription")
    lectures: Mapped[List["Lecture"]] = relationship(
        "Lecture", back_populates="artist", lazy="joined"
    )


class Subscription(Base):
    id = Column(Integer, primary_key=True)
    is_individual = Column(Boolean, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    __tablename__ = "subscription"


class Lecture(Base):
    id = Column(Integer, primary_key=True)
    artist_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    length_sec = Column(Integer, nullable=False)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    # for orm
    artist: Mapped[User] = relationship("User", back_populates="lectures")
    lessons: Mapped[List["Lesson"]] = relationship("Lesson", back_populates="lecture")

    __tablename__ = "lecture"


class Lesson(Base):
    id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, ForeignKey("lecture.id"), nullable=False)
    title = Column(String, nullable=False)
    sheetmusic_img = Column(String, nullable=False)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    # for orm
    lecture: Mapped[Lecture] = relationship("Lecture", back_populates="lessons")
    playlists = relationship(
        "Playlist", secondary="playlist_x_lesson", back_populates="lessons"
    )
    artist = association_proxy("lecture", "artist")

    __tablename__ = "lesson"
