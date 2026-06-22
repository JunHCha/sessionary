from app.core.models import BaseModel


class LessonProgressItem(BaseModel):
    lesson_id: int
    percent: int
    completed: bool
    last_position_sec: int


class LectureProgressData(BaseModel):
    completed_count: int
    total_count: int
    percent: int
    next_lesson_id: int | None
    completed_lesson_ids: list[int]
    lessons: list[LessonProgressItem]
    resume_lesson_id: int | None
    resume_position_sec: int


class PositionReport(BaseModel):
    position_sec: int
    duration_sec: int
