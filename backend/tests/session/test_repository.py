import datetime
import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture, Lesson, User
from app.session.models import SessionType
from app.session.repository import SessionRepository

pytest_plugins = ["tests.conftest"]


@pytest.fixture
async def test_artist(test_session: AsyncSession) -> User:
    now = datetime.datetime.now()
    artist = User(
        id=uuid.uuid4(),
        subscription_id=None,
        time_created=now,
        time_updated=now,
        email="artist@test.com",
        nickname="artist",
        hashed_password="password",
        is_artist=True,
        is_superuser=False,
        is_active=True,
    )
    async with test_session.begin():
        test_session.add(artist)
        await test_session.flush()
    await test_session.commit()
    return artist


@pytest.fixture
async def test_lecture(test_session: AsyncSession, test_artist: User) -> Lecture:
    now = datetime.datetime.now()
    lecture = Lecture(
        id=100,
        artist_id=test_artist.id,
        thumbnail="thumb.png",
        title="Test Lecture",
        description="Description",
        tags=None,
        length_sec=600,
        lecture_count=3,
        time_created=now,
        time_updated=now,
    )
    async with test_session.begin():
        test_session.add(lecture)
        await test_session.flush()
    await test_session.commit()
    return lecture


@pytest.fixture
async def test_lessons(
    test_session: AsyncSession, test_lecture: Lecture, test_artist: User
) -> list[Lesson]:
    now = datetime.datetime.now()
    lessons = [
        Lesson(
            id=101,
            title="Session 1",
            artist_id=test_artist.id,
            lecture_id=test_lecture.id,
            length_sec=100,
            sheetmusic_url="sheet1.gp",
            video_url="video1.mp4",
            text="text1",
            lecture_ordering=1,
            session_type=SessionType.PLAY,
            subtitles=[{"timestamp_ms": 0, "text": "Start"}],
            playing_guide=[],
            sync_offset=0,
            time_created=now,
            time_updated=now,
        ),
        Lesson(
            id=102,
            title="Session 2",
            artist_id=test_artist.id,
            lecture_id=test_lecture.id,
            length_sec=200,
            sheetmusic_url="",
            video_url="video2.mp4",
            text="text2",
            lecture_ordering=2,
            session_type=SessionType.TALK,
            subtitles=None,
            playing_guide=None,
            sync_offset=100,
            time_created=now,
            time_updated=now,
        ),
        Lesson(
            id=103,
            title="Session 3",
            artist_id=test_artist.id,
            lecture_id=test_lecture.id,
            length_sec=150,
            sheetmusic_url="sheet3.gp",
            video_url="",
            text="text3",
            lecture_ordering=3,
            session_type=None,
            subtitles=None,
            playing_guide=None,
            sync_offset=0,
            time_created=now,
            time_updated=now,
        ),
    ]
    async with test_session.begin():
        for lesson in lessons:
            test_session.add(lesson)
        await test_session.flush()
    await test_session.commit()
    return lessons


class TestSessionRepository:
    async def test_sut_get_session_detail_returns_session_with_lecture(
        self, stub_sess_manager, test_lessons: list[Lesson]
    ):
        repo = SessionRepository(stub_sess_manager)
        session = await repo.get_session_detail(101)

        assert session is not None
        assert session.id == 101
        assert session.title == "Session 1"
        assert session.lecture is not None
        assert session.lecture.title == "Test Lecture"

    async def test_sut_get_session_detail_returns_none_for_nonexistent(
        self, stub_sess_manager
    ):
        repo = SessionRepository(stub_sess_manager)
        session = await repo.get_session_detail(9999)

        assert session is None

    async def test_sut_get_adjacent_sessions_returns_prev_and_next(
        self, stub_sess_manager, test_lessons: list[Lesson]
    ):
        repo = SessionRepository(stub_sess_manager)
        prev_id, next_id = await repo.get_adjacent_sessions(102, 100)

        assert prev_id == 101
        assert next_id == 103

    async def test_sut_get_adjacent_sessions_returns_none_for_first(
        self, stub_sess_manager, test_lessons: list[Lesson]
    ):
        repo = SessionRepository(stub_sess_manager)
        prev_id, next_id = await repo.get_adjacent_sessions(101, 100)

        assert prev_id is None
        assert next_id == 102

    async def test_sut_get_adjacent_sessions_returns_none_for_last(
        self, stub_sess_manager, test_lessons: list[Lesson]
    ):
        repo = SessionRepository(stub_sess_manager)
        prev_id, next_id = await repo.get_adjacent_sessions(103, 100)

        assert prev_id == 102
        assert next_id is None

    async def test_sut_count_sessions_in_lecture(
        self, stub_sess_manager, test_lessons: list[Lesson]
    ):
        repo = SessionRepository(stub_sess_manager)
        count = await repo.count_sessions_in_lecture(100)

        assert count == 3
