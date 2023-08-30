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
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, relationship

from app.db.base import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


def random_nickname():
    return "".join(random.choices(string.ascii_lowercase, k=5))


class User(SQLAlchemyBaseUserTableUUID, Base):
    nickname = Column(String, default=random_nickname, unique=True, nullable=False)
    is_artist = Column(Boolean, default=False, nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscription.id"), nullable=True)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    # for orm
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    subscription: Mapped["Subscription"] = relationship("Subscription")
    lectures: Mapped[List["Lecture"]] = relationship(
        "Lecture", secondary="artist_x_lecture", back_populates="artists"
    )
    playlists: Mapped[List["Playlist"]] = relationship(
        "Playlist", back_populates="owner"
    )
    lessons: Mapped[List["Lesson"]] = relationship("Lesson", back_populates="artist")


class Subscription(Base):
    id = Column(Integer, primary_key=True)
    is_individual = Column(Boolean, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    __tablename__ = "subscription"


class Lecture(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artists = Column(String, nullable=False)
    description = Column(String, nullable=False)
    length_sec = Column(Integer, default=0, nullable=False)
    lecture_count = Column(Integer, default=0, nullable=False)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    # for orm
    artists: Mapped[List[User]] = relationship(
        "User", secondary="artist_x_lecture", back_populates="lectures"
    )
    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson", secondary="lecture_x_lesson", back_populates="lectures"
    )

    __tablename__ = "lecture"


class Playlist(Base):
    id = Column(Integer, primary_key=True)
    owner_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    length_sec = Column(Integer, nullable=False)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    # for orm
    owner: Mapped[User] = relationship("User", back_populates="playlists")
    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson", secondary="playlist_x_lesson", back_populates="playlists"
    )

    __tablename__ = "playlist"


class Lesson(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    sheetmusic_url = Column(String)
    video_url = Column(String)
    text = Column(String)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    # for orm
    lectures: Mapped[List[Lecture]] = relationship(
        "Lecture", secondary="lecture_x_lesson", back_populates="lessons"
    )
    playlists: Mapped[List[Playlist]] = relationship(
        "Playlist", secondary="playlist_x_lesson", back_populates="lessons"
    )
    artist: Mapped[User] = relationship("User", back_populates="lessons")

    __tablename__ = "lesson"


class ArtistXLecture(Base):
    artist_id = Column(UUID, ForeignKey("user.id"), primary_key=True)
    lecture_id = Column(Integer, ForeignKey("lecture.id"), primary_key=True)

    __tablename__ = "artist_x_lecture"


class LectureXLesson(Base):
    lecture_id = Column(Integer, ForeignKey("lecture.id"), primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lesson.id"), primary_key=True)

    __tablename__ = "lecture_x_lesson"


class PlaylistXLesson(Base):
    playlist_id = Column(Integer, ForeignKey("playlist.id"), primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lesson.id"), primary_key=True)

    __tablename__ = "playlist_x_lesson"
