from app.core.models import BaseModel


class LectureProgressData(BaseModel):
    completed_count: int
    total_count: int
    percent: int
    next_lesson_id: int | None
    completed_lesson_ids: list[int]
