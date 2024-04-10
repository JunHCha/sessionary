import abc

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependency import get_session


class BaseLectureRepository(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class LectureRepository(BaseLectureRepository): ...


def get_lecture_repository(session=Depends(get_session)) -> BaseLectureRepository:
    return LectureRepository(session=session)
