import datetime

from app.db import tables as tb
from app.lecture.models import LectureDetail
from app.lesson.models import LessonInLecture
from app.progress.repository import ProgressRepository
from app.progress.service import ProgressService


def _build_lecture_detail() -> LectureDetail:
    now = datetime.datetime.now()
    lessons = [
        LessonInLecture(
            id=700 + i,
            title=f"lesson{i}",
            length_sec=60,
            lecture_ordering=i,
            time_created=now,
            time_updated=now,
        )
        for i in range(3)
    ]
    return LectureDetail(
        id=600,
        title="pl-lecture",
        artist=None,
        lessons=lessons,
        description="desc",
        thumbnail="t.png",
        tags=("원곡카피", "Easy"),
        length_sec=0,
        lecture_count=3,
        time_created=now,
        time_updated=now,
    )


async def test_progress_zero_when_nothing_completed(
    progress_service: ProgressService,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    result = await progress_service.get_lecture_progress(
        test_user.id, _build_lecture_detail()
    )
    assert result.completed_count == 0
    assert result.total_count == 3
    assert result.percent == 0
    assert result.next_lesson_id == 700
    assert result.completed_lesson_ids == []


async def test_progress_partial_next_is_first_incomplete(
    progress_service: ProgressService,
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    await progress_repository.mark_complete(test_user.id, 700)
    result = await progress_service.get_lecture_progress(
        test_user.id, _build_lecture_detail()
    )
    assert result.completed_count == 1
    assert result.percent == 33
    assert result.next_lesson_id == 701
    assert result.completed_lesson_ids == [700]


async def test_progress_all_complete_next_is_none(
    progress_service: ProgressService,
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    for lid in (700, 701, 702):
        await progress_repository.mark_complete(test_user.id, lid)
    result = await progress_service.get_lecture_progress(
        test_user.id, _build_lecture_detail()
    )
    assert result.completed_count == 3
    assert result.percent == 100
    assert result.next_lesson_id is None
