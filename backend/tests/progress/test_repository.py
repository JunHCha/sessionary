from app.db import tables as tb
from app.progress.repository import ProgressRepository

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


async def test_mark_complete_creates_progress(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    progress = await progress_repository.mark_complete(test_user.id, 700)
    assert progress.lesson_id == 700
    assert progress.lecture_id == 600

    ids = await progress_repository.get_completed_lesson_ids(test_user.id, 600)
    assert ids == [700]


async def test_mark_complete_is_idempotent(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    await progress_repository.mark_complete(test_user.id, 700)
    await progress_repository.mark_complete(test_user.id, 700)

    ids = await progress_repository.get_completed_lesson_ids(test_user.id, 600)
    assert ids == [700]


async def test_get_completed_lesson_ids_empty(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    ids = await progress_repository.get_completed_lesson_ids(test_user.id, 600)
    assert ids == []


async def test_unmark_removes_progress(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    await progress_repository.mark_complete(test_user.id, 700)
    await progress_repository.unmark(test_user.id, 700)

    ids = await progress_repository.get_completed_lesson_ids(test_user.id, 600)
    assert ids == []


async def test_upsert_position_creates_row(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    row = await progress_repository.upsert_position(test_user.id, 700, 30, 60)
    assert row.lesson_id == 700
    assert row.lecture_id == 600
    assert row.last_position_sec == 30
    assert row.duration_sec == 60
    assert row.progress_percent == 50
    assert row.completed_at is None


async def test_upsert_position_is_monotonic(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    await progress_repository.upsert_position(test_user.id, 700, 50, 60)
    row = await progress_repository.upsert_position(test_user.id, 700, 10, 60)
    # 위치는 갱신되지만 누적 시청률은 내려가지 않는다
    assert row.last_position_sec == 10
    assert row.progress_percent == 83


async def test_upsert_position_completes_at_threshold(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    row = await progress_repository.upsert_position(test_user.id, 700, 54, 60)
    assert row.progress_percent == 90
    assert row.completed_at is not None


async def test_upsert_position_below_threshold_not_completed(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    row = await progress_repository.upsert_position(test_user.id, 700, 53, 60)
    assert row.progress_percent == 88
    assert row.completed_at is None


async def test_upsert_position_completed_at_stable_after_complete(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    first = await progress_repository.upsert_position(test_user.id, 700, 60, 60)
    assert first.completed_at is not None
    completed_at = first.completed_at
    second = await progress_repository.upsert_position(test_user.id, 700, 5, 60)
    assert second.completed_at == completed_at


async def test_upsert_position_zero_duration_guard(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    row = await progress_repository.upsert_position(test_user.id, 700, 10, 0)
    assert row.progress_percent == 0
    assert row.completed_at is None


async def test_get_progress_rows_returns_all(
    progress_repository: ProgressRepository,
    test_user: tb.User,
    lecture_with_lessons: tb.Lecture,
):
    await progress_repository.upsert_position(test_user.id, 700, 30, 60)
    await progress_repository.mark_complete(test_user.id, 701)
    rows = await progress_repository.get_progress_rows(test_user.id, 600)
    by_lesson = {r.lesson_id: r for r in rows}
    assert set(by_lesson) == {700, 701}
    assert by_lesson[700].completed_at is None
    assert by_lesson[701].completed_at is not None
