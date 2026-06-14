import datetime
import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import tables as tb

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def progress_lecture(test_session: AsyncSession) -> tb.Lecture:
    now = datetime.datetime.now()
    artist = tb.User(
        id=uuid.uuid4(),
        time_created=now,
        time_updated=now,
        email="prog-artist@test.com",
        nickname="prog-artist",
        hashed_password="password",
        is_artist=True,
        is_superuser=False,
        is_active=True,
    )
    lecture = tb.Lecture(
        id=500,
        artist_id=artist.id,
        thumbnail="t.png",
        title="prog-lecture",
        description="desc",
        tags=("원곡카피", "Easy"),
        length_sec=0,
        time_created=now,
        time_updated=now,
    )
    lesson = tb.Lesson(
        id=900,
        title="lesson1",
        artist_id=artist.id,
        lecture_id=lecture.id,
        length_sec=60,
        sheetmusic_url="",
        video_url="",
        text="",
        lecture_ordering=0,
    )
    async with test_session.begin():
        test_session.add_all([artist, lecture, lesson])
        await test_session.flush()
    await test_session.commit()
    return lecture


async def test_lesson_progress_row_persists(
    test_user: tb.User, progress_lecture: tb.Lecture, test_session: AsyncSession
):
    progress = tb.LessonProgress(
        user_id=test_user.id,
        lesson_id=900,
        lecture_id=progress_lecture.id,
    )
    async with test_session.begin():
        test_session.add(progress)
        await test_session.flush()
    await test_session.commit()

    result = await test_session.execute(
        select(tb.LessonProgress).where(tb.LessonProgress.user_id == test_user.id)
    )
    saved = result.scalar_one()
    assert saved.lesson_id == 900
    assert saved.lecture_id == progress_lecture.id
    assert saved.completed_at is not None


async def test_lesson_progress_unique_user_lesson(
    test_user: tb.User, progress_lecture: tb.Lecture, test_session: AsyncSession
):
    async with test_session.begin():
        test_session.add(
            tb.LessonProgress(
                user_id=test_user.id, lesson_id=900, lecture_id=progress_lecture.id
            )
        )
        await test_session.flush()
    await test_session.commit()

    with pytest.raises(IntegrityError):
        async with test_session.begin():
            test_session.add(
                tb.LessonProgress(
                    user_id=test_user.id,
                    lesson_id=900,
                    lecture_id=progress_lecture.id,
                )
            )
            await test_session.flush()
