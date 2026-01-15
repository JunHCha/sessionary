import abc

from sqlalchemy import select
from sqlalchemy.orm import joinedload, lazyload

from app.db import tables as tb
from app.db.session import SessionManager
from app.lecture.models import LectureInList
from app.user.models import UserArtistInfo


class BaseUserRepository(abc.ABC):
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    @abc.abstractmethod
    async def get_artists(self) -> list[UserArtistInfo]:
        raise NotImplementedError


class UserRepository(BaseUserRepository):
    async def get_artists(self) -> list[UserArtistInfo]:
        async with self._session_manager.async_session() as session:
            results = (
                (
                    await session.execute(
                        select(tb.User)
                        .options(
                            joinedload(tb.User.lectures).joinedload(tb.Lecture.lessons),
                            joinedload(tb.User.lectures).joinedload(tb.Lecture.artist),
                            lazyload(tb.User.oauth_accounts),
                            lazyload(tb.User.subscription),
                            lazyload(tb.User.lessons),
                        )
                        .filter(tb.User.is_artist.is_(True))
                    )
                )
                .unique()
                .scalars()
                .all()
            )
            return self._map_to_artist_info(results)

    def _map_to_artist_info(self, results) -> list[UserArtistInfo]:
        from app.lecture.models import ArtistInfoInLecture
        from app.lesson.models import LessonInLecture

        return [
            UserArtistInfo(
                id=row.id,
                nickname=row.nickname,
                time_created=row.time_created,
                lectures=[
                    LectureInList(
                        id=lecture.id,
                        thumbnail=lecture.thumbnail,
                        title=lecture.title,
                        artist=ArtistInfoInLecture(
                            id=lecture.artist.id,
                            nickname=lecture.artist.nickname,
                            is_artist=lecture.artist.is_artist,
                        )
                        if lecture.artist
                        else None,
                        lessons=[
                            LessonInLecture(
                                id=lesson.id,
                                title=lesson.title,
                                length_sec=lesson.length_sec,
                                lecture_ordering=lesson.lecture_ordering,
                                time_created=lesson.time_created,
                                time_updated=lesson.time_updated,
                            )
                            for lesson in lecture.lessons
                        ],
                        description=lecture.description,
                        tags=lecture.tags,
                        length_sec=lecture.length_sec,
                        lecture_count=lecture.lecture_count,
                        time_created=lecture.time_created,
                        time_updated=lecture.time_updated,
                    )
                    for lecture in row.lectures
                ],
            )
            for row in results
        ]
