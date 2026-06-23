import uuid

from app.db import tables as tb
from app.lecture.models import LectureDetail
from app.lecture.service import BaseLectureService
from app.progress.models import LectureProgressData, LessonProgressItem
from app.progress.repository import BaseProgressRepository


class ProgressService:
    def __init__(
        self,
        repository: BaseProgressRepository,
        lecture_service: BaseLectureService,
    ) -> None:
        self.repository = repository
        self.lecture_service = lecture_service

    async def get_lecture_progress(
        self, user_id: uuid.UUID, lecture: LectureDetail
    ) -> LectureProgressData:
        lessons = sorted(lecture.lessons, key=lambda lesson: lesson.lecture_ordering)
        lesson_ids = [lesson.id for lesson in lessons]
        total_count = len(lessons)

        rows = await self.repository.get_progress_rows(user_id, lecture.id)
        rows_by_lesson = {row.lesson_id: row for row in rows}

        lesson_items: list[LessonProgressItem] = []
        completed_lesson_ids: list[int] = []
        for lesson_id in lesson_ids:
            row = rows_by_lesson.get(lesson_id)
            completed = row is not None and row.completed_at is not None
            if completed:
                completed_lesson_ids.append(lesson_id)
            lesson_items.append(
                LessonProgressItem(
                    lesson_id=lesson_id,
                    percent=row.progress_percent if row is not None else 0,
                    completed=completed,
                    last_position_sec=row.last_position_sec if row is not None else 0,
                )
            )

        completed_count = len(completed_lesson_ids)
        percent = (
            round(completed_count / total_count * 100) if total_count > 0 else 0
        )

        completed_set = set(completed_lesson_ids)
        resume_lesson_id = next(
            (lid for lid in lesson_ids if lid not in completed_set), None
        )
        resume_row = (
            rows_by_lesson.get(resume_lesson_id)
            if resume_lesson_id is not None
            else None
        )
        resume_position_sec = (
            resume_row.last_position_sec if resume_row is not None else 0
        )

        return LectureProgressData(
            completed_count=completed_count,
            total_count=total_count,
            percent=percent,
            next_lesson_id=resume_lesson_id,
            completed_lesson_ids=completed_lesson_ids,
            lessons=lesson_items,
            resume_lesson_id=resume_lesson_id,
            resume_position_sec=resume_position_sec,
        )

    async def mark_complete(
        self, user_id: uuid.UUID, lesson_id: int
    ) -> tb.LessonProgress:
        return await self.repository.mark_complete(user_id, lesson_id)

    async def report_position(
        self,
        user_id: uuid.UUID,
        lesson_id: int,
        position_sec: int,
        duration_sec: int,
    ) -> LectureProgressData:
        progress = await self.repository.upsert_position(
            user_id, lesson_id, position_sec, duration_sec
        )
        lecture = await self.lecture_service.get_lecture_detail(progress.lecture_id)
        return await self.get_lecture_progress(user_id, lecture)
