import datetime
import random
import string
import uuid
from typing import List

from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


def random_nickname():
    return "".join(random.choices(string.ascii_lowercase, k=5))


class User(SQLAlchemyBaseUserTableUUID, Base):
    nickname: Mapped[str] = mapped_column(
        String, default=random_nickname, unique=True, nullable=False
    )
    is_artist: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    experienced: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    subscription_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID, ForeignKey("subscription.id"), nullable=True
    )
    time_created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )
    time_updated: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # for orm
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    subscription: Mapped["Subscription"] = relationship(
        "Subscription",
        secondary="user_x_subscription",
        secondaryjoin="and_(user_x_subscription.c.subscription_id == subscription.c.id,"
        "subscription.c.is_active == True)",
        back_populates="subscribers",
        lazy="subquery",
    )
    lectures: Mapped[List["Lecture"]] = relationship(
        "Lecture", secondary="artist_x_lecture"
    )
    playlists: Mapped[List["Playlist"]] = relationship(
        "Playlist", back_populates="owner"
    )
    lessons: Mapped[List["Lesson"]] = relationship("Lesson", back_populates="artist")


class Subscription(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(String, nullable=False, default="ticket")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    ticket_count: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    time_created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )

    # for orm
    subscribers: Mapped[List[User]] = relationship(
        "User",
        secondary="user_x_subscription",
        back_populates="subscription",
        uselist=True,
    )

    __tablename__ = "subscription"


class Lecture(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=False)
    length_sec: Mapped[int] = Column(Integer, default=0, nullable=False)
    lecture_count: Mapped[int] = Column(Integer, default=0, nullable=False)
    time_created: Mapped[datetime.datetime] = Column(DateTime, default=func.now())
    time_updated: Mapped[datetime.datetime] = Column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # for orm
    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson",
        secondary="lecture_x_lesson",
        back_populates="lecture",
        uselist=True,
        order_by="lecture_x_lesson.c.ordering",
        lazy="selectin",
    )

    __tablename__ = "lecture"


class Playlist(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("user.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    length_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    time_created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )
    time_updated: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # for orm
    owner: Mapped[User] = relationship("User", back_populates="playlists")
    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson", secondary="playlist_x_lesson", back_populates="playlists"
    )

    __tablename__ = "playlist"


class Lesson(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    artist_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("user.id"), nullable=False
    )
    lecture_id: Mapped[int] = mapped_column(Integer, ForeignKey("lecture.id"))
    sheetmusic_url: Mapped[str] = mapped_column(String)
    video_url: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    time_created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )
    time_updated: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # for orm
    lecture: Mapped[Lecture] = relationship("Lecture", back_populates="lessons")
    playlists: Mapped[List[Playlist]] = relationship(
        "Playlist",
        secondary="playlist_x_lesson",
        back_populates="lessons",
        lazy="selectin",
    )
    artist: Mapped[User] = relationship("User", back_populates="lessons")

    __tablename__ = "lesson"


class UserXSubscription(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("user.id"))
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("subscription.id")
    )

    __tablename__ = "user_x_subscription"


class ArtistXLecture(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    artist_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("user.id"))
    lecture_id: Mapped[int] = mapped_column(Integer, ForeignKey("lecture.id"))

    __tablename__ = "artist_x_lecture"


class LectureXLesson(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lecture_id: Mapped[int] = mapped_column(Integer, ForeignKey("lecture.id"))
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey("lesson.id"))
    ordering: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __tablename__ = "lecture_x_lesson"


class PlaylistXLesson(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    playlist_id: Mapped[int] = mapped_column(Integer, ForeignKey("playlist.id"))
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey("lesson.id"))

    __tablename__ = "playlist_x_lesson"
