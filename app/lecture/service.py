import abc
import uuid

from app.lecture.repository import BaseLectureRepository
from app.models import Lecture, Lesson


class BaseLectureService(abc.ABC):
    def __init__(self, repository: BaseLectureRepository) -> None:
        self.user_repository = repository

    @abc.abstractmethod
    async def get_recommended(
        self, artist_id: uuid.UUID | None = None
    ) -> list[Lecture]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_lessons(self, lecture_id: int) -> list[any]:
        raise NotImplementedError


class LectureService(BaseLectureService):
    async def get_recommended(
        self, artist_id: uuid.UUID | None = None
    ) -> list[Lecture]:
        return []

    async def get_lessons(self, lecture_id: int) -> list[Lesson]:
        raise []
