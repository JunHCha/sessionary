import abc

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, lazyload

from app.db import tables as tb
from app.lecture.models import LectureInList
from app.user.models import UserArtistInfo


class BaseUserRepository(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abc.abstractmethod
    async def get_artists(self) -> list[UserArtistInfo]:
        raise NotImplementedError


class UserRepository(BaseUserRepository):
    async def get_artists(self) -> list[UserArtistInfo]:
        results = (
            (
                await self.session.execute(
                    select(tb.User)
                    .options(
                        joinedload(tb.User.lectures),
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
                        artist=lecture.artist.nickname if lecture.artist else None,
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
