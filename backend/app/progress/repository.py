import abc
import uuid

from sqlalchemy import delete, func, select

from app.db import tables as tb
from app.db.session import SessionManager

COMPLETION_THRESHOLD_PERCENT = 90


class BaseProgressRepository(abc.ABC):
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    @abc.abstractmethod
    async def upsert_position(
        self,
        user_id: uuid.UUID,
        lesson_id: int,
        position_sec: int,
        duration_sec: int,
    ) -> tb.LessonProgress:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_progress_rows(
        self, user_id: uuid.UUID, lecture_id: int
    ) -> list[tb.LessonProgress]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_completed_lesson_ids(
        self, user_id: uuid.UUID, lecture_id: int
    ) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def mark_complete(
        self, user_id: uuid.UUID, lesson_id: int
    ) -> tb.LessonProgress:
        raise NotImplementedError

    @abc.abstractmethod
    async def unmark(self, user_id: uuid.UUID, lesson_id: int) -> None:
        raise NotImplementedError


class ProgressRepository(BaseProgressRepository):
    async def get_completed_lesson_ids(
        self, user_id: uuid.UUID, lecture_id: int
    ) -> list[int]:
        async with self._session_manager.async_session() as session:
            result = await session.execute(
                select(tb.LessonProgress.lesson_id).where(
                    tb.LessonProgress.user_id == user_id,
                    tb.LessonProgress.lecture_id == lecture_id,
                    tb.LessonProgress.completed_at.is_not(None),
                )
            )
            return list(result.scalars().all())

    async def mark_complete(
        self, user_id: uuid.UUID, lesson_id: int
    ) -> tb.LessonProgress:
        async with self._session_manager.async_session() as session:
            existing = await session.execute(
                select(tb.LessonProgress).where(
                    tb.LessonProgress.user_id == user_id,
                    tb.LessonProgress.lesson_id == lesson_id,
                )
            )
            progress = existing.scalar_one_or_none()
            if progress is not None:
                return progress

            lecture_id = (
                await session.execute(
                    select(tb.Lesson.lecture_id).where(tb.Lesson.id == lesson_id)
                )
            ).scalar_one()

            progress = tb.LessonProgress(
                user_id=user_id,
                lesson_id=lesson_id,
                lecture_id=lecture_id,
                progress_percent=100,
                completed_at=func.now(),
            )
            session.add(progress)
            await session.flush()
            await session.commit()
            await session.refresh(progress)
            return progress

    async def unmark(self, user_id: uuid.UUID, lesson_id: int) -> None:
        async with self._session_manager.async_session() as session:
            await session.execute(
                delete(tb.LessonProgress).where(
                    tb.LessonProgress.user_id == user_id,
                    tb.LessonProgress.lesson_id == lesson_id,
                )
            )
            await session.commit()

    async def upsert_position(
        self,
        user_id: uuid.UUID,
        lesson_id: int,
        position_sec: int,
        duration_sec: int,
    ) -> tb.LessonProgress:
        new_percent = (
            round(position_sec / duration_sec * 100) if duration_sec > 0 else 0
        )

        async with self._session_manager.async_session() as session:
            existing = await session.execute(
                select(tb.LessonProgress).where(
                    tb.LessonProgress.user_id == user_id,
                    tb.LessonProgress.lesson_id == lesson_id,
                )
            )
            progress = existing.scalar_one_or_none()

            if progress is None:
                lecture_id = (
                    await session.execute(
                        select(tb.Lesson.lecture_id).where(tb.Lesson.id == lesson_id)
                    )
                ).scalar_one()
                progress = tb.LessonProgress(
                    user_id=user_id,
                    lesson_id=lesson_id,
                    lecture_id=lecture_id,
                    progress_percent=0,
                )
                session.add(progress)

            progress.last_position_sec = position_sec
            progress.duration_sec = duration_sec
            progress.progress_percent = max(progress.progress_percent, new_percent)

            if (
                progress.progress_percent >= COMPLETION_THRESHOLD_PERCENT
                and progress.completed_at is None
            ):
                progress.completed_at = func.now()

            await session.flush()
            await session.commit()
            await session.refresh(progress)
            return progress

    async def get_progress_rows(
        self, user_id: uuid.UUID, lecture_id: int
    ) -> list[tb.LessonProgress]:
        async with self._session_manager.async_session() as session:
            result = await session.execute(
                select(tb.LessonProgress).where(
                    tb.LessonProgress.user_id == user_id,
                    tb.LessonProgress.lecture_id == lecture_id,
                )
            )
            return list(result.scalars().all())
