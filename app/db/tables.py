from typing import List

from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Mapped,
    String,
    UniqueConstraint,
    relationship,
)
from sqlalchemy.ext.associationproxy import association_proxy

from app.db.session.base import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    nickname: str = Column(String, unique=True, nullable=False)

    # for orm
    subscription: Mapped["Subscription"] = relationship(
        "Subscription", back_populates="user"
    )


class Subscription(Base):
    id = Column(Integer, primary_key=True)
    type: str = Column(Enum("trial", "personal", "bundle", name="subscription_type"))
    is_active = Column(Boolean, nullable=False)
    expire_at = Column(DateTime, nullable=False)

    # for orm
    user: Mapped[User] = relationship("User", back_populates="subscription")

    __tablename__ = "subscription"
    __constraints__ = (
        UniqueConstraint("user_id", "id", name="uq_subscription_user_id_id"),
    )


class Artist(SQLAlchemyBaseUserTableUUID, Base):
    # TODO: Artist, Lecture, Lesson 간의 M:N relation 모호함
    nickname: str = Column(String, unique=True, nullable=False)

    # for orm
    lectures: List[Mapped["Lecture"]] = relationship(
        "Lecture", back_populates="artist", lazy="joined"
    )

    __tablename__ = "artist"


class Lecture(Base):
    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey("artist.id"), nullable=False)
    title: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)
    length_sec: int = Column(Integer, nullable=False)

    # for orm
    artist: Mapped[Artist] = relationship("Artist", back_populates="lectures")
    lessons: List[Mapped["Lesson"]] = relationship()

    __tablename__ = "lecture"


class Lesson(Base):
    id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, nullable=False)
    title: str = Column(String, nullable=False)
    sheetmusic_img: str = Column(String, nullable=False)

    # for orm
    lecture: Mapped[Lecture] = relationship("Lecture")
    artist: Mapped[Artist] = association_proxy("lecture", "artist")

    __tablename__ = "lesson"
