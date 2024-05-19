import datetime
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture, Lesson, User


@pytest.fixture
async def dummy_lectures(test_session: AsyncSession) -> None:
    now = datetime.datetime.now()
    artist_1 = User(
        id=uuid.uuid4(),
        subscription_id=None,
        time_created=now,
        time_updated=now,
        email="artist1@test.com",
        nickname="artist1",
        hashed_password="password",
        is_artist=True,
        is_superuser=False,
        is_active=True,
    )
    artist_2 = User(
        id=uuid.uuid4(),
        subscription_id=None,
        time_created=now,
        time_updated=now,
        email="artist2@test.com",
        nickname="artist2",
        hashed_password="password",
        is_artist=True,
        is_superuser=False,
        is_active=True,
    )
    lectures = [
        Lecture(
            id=num,
            title=f"lecture{num - 9}",
            description=f"description{num - 9}",
            length_sec=0,
            time_created=now,
            time_updated=now,
        )
        for num in range(10, 110)
    ]
    lessons = [
        Lesson(
            id=num,
            title=f"lesson1-{num - 9}",
            artist_id=artist_1.id,
            lecture_id=10,
            sheetmusic_url=f"file://tab.lecture1-{num - 9}",
            video_url=f"https://video.lecture1-{num - 9}",
            text=f"leeson1-{num - 9} description",
        )
        for num in range(10, 15)
    ] + [
        Lesson(
            id=num,
            title=f"lesson2-{num - 9}",
            artist_id=artist_2.id,
            lecture_id=11,
            sheetmusic_url=f"file://tab.lecture2-{num - 9}",
            video_url=f"https://video.lecture2-{num - 9}",
            text=f"leeson2-{num - 9} description",
        )
        for num in range(15, 20)
    ]

    async with test_session.begin():
        test_session.add_all([artist_1, artist_2] + lectures + lessons)
    await test_session.commit()


async def test_sut_fetch_recommended_lectures(client: AsyncClient, dummy_lectures):
    assert True


async def test_sut_fetch_lessons_in_lecture(client: AsyncClient, dummy_lectures):
    assert True
