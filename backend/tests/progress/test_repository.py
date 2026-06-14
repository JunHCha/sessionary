from app.db import tables as tb
from app.progress.repository import ProgressRepository


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
