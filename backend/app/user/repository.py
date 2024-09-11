import abc

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, lazyload

from app import models
from app.db import tables as tb


class BaseUserRepository(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abc.abstractmethod
    async def get_artists(self) -> list[models.UserArtistInfo]:
        raise NotImplementedError


class UserRepository(BaseUserRepository):
    async def get_artists(self) -> list[models.UserArtistInfo]:
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
            models.UserArtistInfo(
                id=row.id,
                nickname=row.nickname,
                time_created=row.time_created,
                lectures=[lecture for lecture in row.lectures],
            )
            for row in results
        ]
