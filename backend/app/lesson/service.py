from app.db import tables as tb
from app.lesson.models import LessonAdminDetail
from app.lesson.repository import BaseLessonRepository
from app.sheetmusic.service import SheetmusicProvider
from app.video.service import VideoProvider


class LessonService:
    def __init__(
        self,
        repository: BaseLessonRepository,
        video_provider: VideoProvider,
        sheetmusic_provider: SheetmusicProvider,
    ) -> None:
        self.repository = repository
        self.video_provider = video_provider
        self.sheetmusic_provider = sheetmusic_provider

    async def create_lesson(self, fields: dict) -> LessonAdminDetail:
        lesson = await self.repository.create_lesson(fields)
        return self._to_detail(lesson)

    async def update_lesson(
        self, lesson_id: int, fields: dict
    ) -> LessonAdminDetail | None:
        lesson = await self.repository.update_lesson(lesson_id, fields)
        return self._to_detail(lesson) if lesson else None

    async def set_video(
        self, lesson_id: int, object_name: str, data: bytes, content_type: str
    ) -> LessonAdminDetail | None:
        key = await self.video_provider.upload(object_name, data, content_type)
        return await self.update_lesson(lesson_id, {"video_url": key})

    async def set_sheetmusic(
        self, lesson_id: int, object_name: str, data: bytes, content_type: str
    ) -> LessonAdminDetail | None:
        key = await self.sheetmusic_provider.upload(object_name, data, content_type)
        return await self.update_lesson(lesson_id, {"sheetmusic_url": key})

    def _to_detail(self, lesson: tb.Lesson) -> LessonAdminDetail:
        return LessonAdminDetail(
            id=lesson.id,
            lecture_id=lesson.lecture_id,
            title=lesson.title,
            length_sec=lesson.length_sec,
            text=lesson.text,
            lecture_ordering=lesson.lecture_ordering,
            session_type=lesson.session_type,
            sheetmusic_url=lesson.sheetmusic_url,
            video_url=lesson.video_url,
            sync_offset=lesson.sync_offset,
            subtitles=lesson.subtitles or [],
            playing_guide=lesson.playing_guide or [],
        )
