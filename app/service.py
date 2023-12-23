import abc
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependency import get_session
from app.db.tables import User


class BaseUserService(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abc.abstractmethod
    async def get_artists(self) -> List[User]:
        pass


class UserService(BaseUserService):
    async def get_artists(self) -> List[User]:
        stmt = select(User.id, User.nickname, User.time_created).where(User.is_artist)
        results = (await self.session.execute(stmt)).all()
        return results


def get_user_service(session=Depends(get_session)):
    return UserService(session=session)
