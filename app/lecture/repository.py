import abc

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db import tables as tb
from app.models import (
    Lecture,
    LectureInFetch,
    LessonInLecture,
    PaginationMeta,
    UserReadPublic,
)


class BaseLectureRepository(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abc.abstractmethod
    async def fetch_lectures(
        self, page: int, per_page: int
    ) -> tuple[list[LectureInFetch], PaginationMeta]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_lecture(self, lecture_id: int) -> Lecture:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_lecture(self, title: str, description: str) -> Lecture:
        raise NotImplementedError


class LectureRepository(BaseLectureRepository):
    async def fetch_lectures(
        self, page: int, per_page: int
    ) -> tuple[list[LectureInFetch], PaginationMeta]:
        total_items = (
            await self.session.execute(func.count(tb.Lecture.id))
        ).scalar_one()
        results = (
            (
                await self.session.execute(
                    select(tb.Lecture)
                    .offset(page * per_page)
                    .limit(per_page)
                    .order_by(tb.Lecture.time_updated.desc())
                )
            )
            .unique()
            .scalars()
            .all()
        )
        return (
            [LectureInFetch.model_validate(row) for row in results],
            PaginationMeta(
                total_items=total_items,
                total_pages=(total_items + per_page - 1) // per_page,
                curr_page=page,
                per_page=per_page,
            ),
        )

    async def get_lecture(self, lecture_id: int) -> Lecture:
        result = (
            (
                await self.session.execute(
                    select(tb.Lecture)
                    .options(
                        joinedload(tb.Lecture.lessons).joinedload(tb.Lesson.artist)
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
                lecture=item.lecture,
                artist=UserReadPublic.model_validate(item.artist),
                sheetmusic_url=item.sheetmusic_url,
                video_url=item.video_url,
                text=item.text,
                time_created=item.time_created,
                time_updated=item.time_updated,
            )
            for item in result.lessons
        ]
        return Lecture(
            id=result.id,
            title=result.title,
            lessons=lessons,
            artists=result.artists,
            description=result.description,
            length_sec=result.length_sec,
            time_created=result.time_created,
            time_updated=result.time_updated,
        )

    async def create_lecture(self, title: str, description: str) -> Lecture:
        new_lecture = tb.Lecture(title=title, description=description)
        self.session.add(new_lecture)
        await self.session.flush()
        return Lecture(
            id=new_lecture.id,
            title=new_lecture.title,
            lessons=[],
            artists=[],
            description=new_lecture.description,
            length_sec=new_lecture.length_sec,
            time_created=new_lecture.time_created,
            time_updated=new_lecture.time_updated,
        )
