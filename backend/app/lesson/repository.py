import abc

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import tables as tb
from app.db.session import SessionManager


class BaseLessonRepository(abc.ABC):
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    @abc.abstractmethod
    async def get_lesson(self, lesson_id: int) -> tb.Lesson | None:
        raise NotImplementedError


class LessonRepository(BaseLessonRepository):
    async def get_lesson(self, lesson_id: int) -> tb.Lesson | None:
        async with self._session_manager.async_session() as session:
            result = await session.execute(
                select(tb.Lesson)
                .options(selectinload(tb.Lesson.lecture))
                .where(tb.Lesson.id == lesson_id)
            )
            return result.scalar_one_or_none()
