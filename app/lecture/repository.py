import abc

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import tables as tb
from app.models import LectureInFetch, PaginationMeta


class BaseLectureRepository(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abc.abstractmethod
    async def fetch_lectures(
        self, page: int, per_page: int
    ) -> tuple[list[LectureInFetch], PaginationMeta]:
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
