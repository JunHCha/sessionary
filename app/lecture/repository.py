import abc

from sqlalchemy.ext.asyncio import AsyncSession


class BaseLectureRepository(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class LectureRepository(BaseLectureRepository):
    pass
