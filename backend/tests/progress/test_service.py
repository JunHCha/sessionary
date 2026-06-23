import datetime

from app.db import tables as tb
from app.lecture.models import LectureDetail
from app.lesson.models import LessonInLecture
from app.progress.repository import ProgressRepository
from app.progress.service import ProgressService

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


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
    assert result.resume_lesson_id is None
    assert result.resume_position_sec == 0


async def test_progress_per_lesson_aggregation_and_resume(
    progress_service: ProgressService,
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    await progress_repository.mark_complete(test_user.id, 700)
    await progress_repository.upsert_position(test_user.id, 701, 30, 60)

    result = await progress_service.get_lecture_progress(
        test_user.id, _build_lecture_detail()
    )

    by_lesson = {item.lesson_id: item for item in result.lessons}
    assert by_lesson[700].completed is True
    assert by_lesson[700].percent == 100
    assert by_lesson[701].completed is False
    assert by_lesson[701].percent == 50
    assert by_lesson[701].last_position_sec == 30
    assert by_lesson[702].completed is False
    assert by_lesson[702].percent == 0
    assert by_lesson[702].last_position_sec == 0

    # 헤드라인 percent 는 완료 비율 유지(1/3)
    assert result.completed_count == 1
    assert result.percent == 33
    # resume = 미완료 중 ordering 최소 = 701
    assert result.resume_lesson_id == 701
    assert result.resume_position_sec == 30


async def test_report_position_returns_progress(
    progress_service: ProgressService,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    result = await progress_service.report_position(test_user.id, 701, 30, 60)
    by_lesson = {item.lesson_id: item for item in result.lessons}
    assert by_lesson[701].percent == 50
    assert by_lesson[701].last_position_sec == 30
    assert result.resume_lesson_id == 700
    assert result.total_count == 3
