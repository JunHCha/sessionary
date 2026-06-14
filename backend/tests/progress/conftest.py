import datetime
import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import tables as tb
from app.progress.repository import ProgressRepository
from app.progress.service import ProgressService
from tests.containers import TestSessionManager

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
def progress_repository(stub_sess_manager: TestSessionManager) -> ProgressRepository:
    return ProgressRepository(session_manager=stub_sess_manager)


@pytest.fixture
def progress_service(progress_repository: ProgressRepository) -> ProgressService:
    return ProgressService(repository=progress_repository)


@pytest.fixture
async def lecture_with_lessons(test_session: AsyncSession) -> tb.Lecture:
    now = datetime.datetime.now()
    artist = tb.User(
        id=uuid.uuid4(),
        time_created=now,
        time_updated=now,
        email="pl-artist@test.com",
        nickname="pl-artist",
        hashed_password="password",
        is_artist=True,
        is_superuser=False,
        is_active=True,
    )
    lecture = tb.Lecture(
        id=600,
        artist_id=artist.id,
        thumbnail="t.png",
        title="pl-lecture",
        description="desc",
        tags=("원곡카피", "Easy"),
        length_sec=0,
        lecture_count=3,
        time_created=now,
        time_updated=now,
    )
    lessons = [
        tb.Lesson(
            id=700 + i,
            title=f"lesson{i}",
            artist_id=artist.id,
            lecture_id=lecture.id,
            length_sec=60,
            sheetmusic_url="",
            video_url="",
            text="",
            lecture_ordering=i,
        )
        for i in range(3)
    ]
    async with test_session.begin():
        test_session.add_all([artist, lecture, *lessons])
        await test_session.flush()
    await test_session.commit()
    return lecture
