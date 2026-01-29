import abc

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.db import tables as tb
from app.db.session import SessionManager


class BaseSessionRepository(abc.ABC):
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    @abc.abstractmethod
    async def get_session_detail(self, session_id: int) -> tb.Lesson | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_adjacent_sessions(
        self, session_id: int, lecture_id: int
    ) -> tuple[int | None, int | None]:
        raise NotImplementedError

    @abc.abstractmethod
    async def count_sessions_in_lecture(self, lecture_id: int) -> int:
        raise NotImplementedError


class SessionRepository(BaseSessionRepository):
    async def get_session_detail(self, session_id: int) -> tb.Lesson | None:
        async with self._session_manager.async_session() as session:
            result = await session.execute(
                select(tb.Lesson)
                .options(selectinload(tb.Lesson.lecture))
                .where(tb.Lesson.id == session_id)
            )
            return result.scalar_one_or_none()

    async def get_adjacent_sessions(
        self, session_id: int, lecture_id: int
    ) -> tuple[int | None, int | None]:
        async with self._session_manager.async_session() as session:
            current_result = await session.execute(
                select(tb.Lesson.lecture_ordering).where(
                    tb.Lesson.id == session_id,
                    tb.Lesson.lecture_id == lecture_id,
                )
            )
            current_ordering = current_result.scalar_one_or_none()
            if current_ordering is None:
                return None, None

            prev_result = await session.execute(
                select(tb.Lesson.id)
                .where(
                    tb.Lesson.lecture_id == lecture_id,
                    tb.Lesson.lecture_ordering < current_ordering,
                )
                .order_by(tb.Lesson.lecture_ordering.desc())
                .limit(1)
            )
            prev_id = prev_result.scalar_one_or_none()

            next_result = await session.execute(
                select(tb.Lesson.id)
                .where(
                    tb.Lesson.lecture_id == lecture_id,
                    tb.Lesson.lecture_ordering > current_ordering,
                )
                .order_by(tb.Lesson.lecture_ordering.asc())
                .limit(1)
            )
            next_id = next_result.scalar_one_or_none()

            return prev_id, next_id

    async def count_sessions_in_lecture(self, lecture_id: int) -> int:
        async with self._session_manager.async_session() as session:
            result = await session.execute(
                select(func.count(tb.Lesson.id)).where(
                    tb.Lesson.lecture_id == lecture_id
                )
            )
            return result.scalar_one()
