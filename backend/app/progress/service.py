import uuid

from app.db import tables as tb
from app.lecture.models import LectureDetail
from app.progress.models import LectureProgressData
from app.progress.repository import BaseProgressRepository


class ProgressService:
    def __init__(self, repository: BaseProgressRepository) -> None:
        self.repository = repository

    async def get_lecture_progress(
        self, user_id: uuid.UUID, lecture: LectureDetail
    ) -> LectureProgressData:
        lessons = sorted(lecture.lessons, key=lambda lesson: lesson.lecture_ordering)
        lesson_ids = [lesson.id for lesson in lessons]
        total_count = len(lessons)

        completed_all = await self.repository.get_completed_lesson_ids(
            user_id, lecture.id
        )
        completed_set = set(completed_all)
        completed_lesson_ids = [lid for lid in lesson_ids if lid in completed_set]
        completed_count = len(completed_lesson_ids)

        percent = (
            round(completed_count / total_count * 100) if total_count > 0 else 0
        )

        next_lesson_id = next(
            (lid for lid in lesson_ids if lid not in completed_set), None
        )

        return LectureProgressData(
            completed_count=completed_count,
            total_count=total_count,
            percent=percent,
            next_lesson_id=next_lesson_id,
            completed_lesson_ids=completed_lesson_ids,
        )

    async def mark_complete(
        self, user_id: uuid.UUID, lesson_id: int
    ) -> tb.LessonProgress:
        return await self.repository.mark_complete(user_id, lesson_id)
