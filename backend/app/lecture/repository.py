import abc

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db import tables as tb
from app.lecture.models import LectureDetail, LectureInList, PaginationMeta
from app.lesson.models import LessonInLecture


class BaseLectureRepository(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abc.abstractmethod
    async def fetch_lectures(
        self, page: int, per_page: int
    ) -> tuple[list[LectureInList], PaginationMeta]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_lecture(self, lecture_id: int) -> LectureDetail:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_lecture(self, title: str, description: str) -> LectureDetail:
        raise NotImplementedError


class LectureRepository(BaseLectureRepository):
    async def fetch_lectures(
        self, page: int, per_page: int
    ) -> tuple[list[LectureInList], PaginationMeta]:
        total_items = (
            await self.session.execute(func.count(tb.Lecture.id))
        ).scalar_one()
        results = (
            (
                await self.session.execute(
                    select(tb.Lecture)
                    .offset((page - 1) * per_page)
                    .limit(per_page)
                    .order_by(tb.Lecture.time_updated.desc())
                )
            )
            .unique()
            .scalars()
            .all()
        )
        return (
            [LectureInList.model_validate(row) for row in results],
            PaginationMeta(
                total_items=total_items,
                total_pages=(total_items + per_page - 1) // per_page,
                curr_page=page,
                per_page=per_page,
            ),
        )

    async def get_lecture(self, lecture_id: int) -> LectureDetail:
        result = (
            (
                await self.session.execute(
                    select(tb.Lecture)
                    .options(
                        joinedload(tb.Lecture.artist), joinedload(tb.Lecture.lessons)
                    )
                    .filter(tb.Lecture.id == lecture_id)
                )
            )
            .unique()
            .scalar_one()
        )
        lessons = [
            LessonInLecture(
                id=item.id,
                title=item.title,
                length_sec=item.length_sec,
                lecture_ordering=item.lecture_ordering,
                time_created=item.time_created,
                time_updated=item.time_updated,
            )
            for item in result.lessons
        ]
        return LectureDetail(
            id=result.id,
            title=result.title,
            lessons=lessons,
            artist=result.artist,
            description=result.description,
            length_sec=result.length_sec,
            time_created=result.time_created,
            time_updated=result.time_updated,
        )

    async def create_lecture(self, title: str, description: str) -> LectureDetail:
        new_lecture = tb.Lecture(title=title, description=description)
        self.session.add(new_lecture)
        await self.session.flush()
        await self.session.commit()
        return LectureDetail(
            id=new_lecture.id,
            title=new_lecture.title,
            artist=None,
            lessons=[],
            description=new_lecture.description,
            length_sec=new_lecture.length_sec,
            time_created=new_lecture.time_created,
            time_updated=new_lecture.time_updated,
        )
