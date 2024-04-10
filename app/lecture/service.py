import abc
import uuid

from fastapi import Depends

from app.lecture.models import Lecture
from app.lecture.repository import BaseLectureRepository, get_lecture_repository


class BaseLectureService(abc.ABC):
    def __init__(self, repository: BaseLectureRepository) -> None:
        self.user_repository = repository

    @abc.abstractmethod
    async def get_recommended(
        self, artist_id: uuid.UUID | None = None
    ) -> list[Lecture]:
        raise NotImplementedError


class LectureService(BaseLectureService):
    pass


def get_lecture_service(
    repository: BaseLectureRepository = Depends(get_lecture_repository),
) -> BaseLectureService:
    return LectureService(repository)
