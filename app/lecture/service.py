import abc

from app.lecture.repository import BaseLectureRepository
from app.models import Lecture, LectureInFetch, PaginationMeta


class BaseLectureService(abc.ABC):
    def __init__(self, repository: BaseLectureRepository) -> None:
        self.lecture_repository = repository

    @abc.abstractmethod
    async def get_recommended(
        self, page: int = 1, per_page: int = 20
    ) -> tuple[list[LectureInFetch], PaginationMeta]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_lecture_detail(self, lecture_id: int) -> Lecture:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_lecture(self, title: str, description: str) -> Lecture:
        raise NotImplementedError


class LectureService(BaseLectureService):
    async def get_recommended(
        self, page: int = 1, per_page: int = 20
    ) -> tuple[list[LectureInFetch], PaginationMeta]:
        lectures, pagination_meta = await self.lecture_repository.fetch_lectures(
            page, per_page
        )
        return (lectures, pagination_meta)

    async def get_lecture_detail(self, lecture_id: int) -> Lecture:
        lecture = await self.lecture_repository.get_lecture(lecture_id)
        return lecture

    async def create_lecture(self, title: str, description: str) -> Lecture:
        lecture = await self.lecture_repository.create_lecture(title, description)
        return lecture
