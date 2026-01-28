import datetime
import uuid

from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture, Lesson, Subscription, TicketUsage, User
from app.session.models import SessionType

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def session_artist(test_session: AsyncSession) -> User:
    now = datetime.datetime.now()
    artist = User(
        id=uuid.uuid4(),
        subscription_id=None,
        time_created=now,
        time_updated=now,
        email="session_artist@test.com",
        nickname="session_artist",
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
async def session_lecture(test_session: AsyncSession, session_artist: User) -> Lecture:
    now = datetime.datetime.now()
    lecture = Lecture(
        id=200,
        artist_id=session_artist.id,
        thumbnail="thumb.png",
        title="Session Test Lecture",
        description="Description",
        tags=None,
        length_sec=600,
        lecture_count=2,
        time_created=now,
        time_updated=now,
    )
    async with test_session.begin():
        test_session.add(lecture)
        await test_session.flush()
    await test_session.commit()
    return lecture


@pytest.fixture
async def session_lessons(
    test_session: AsyncSession, session_lecture: Lecture, session_artist: User
) -> list[Lesson]:
    now = datetime.datetime.now()
    lessons = [
        Lesson(
            id=201,
            title="Session 1",
            artist_id=session_artist.id,
            lecture_id=session_lecture.id,
            length_sec=100,
            sheetmusic_url="sheet1.gp",
            video_url="video1.mp4",
            text="text1",
            lecture_ordering=1,
            session_type=SessionType.PLAY,
            subtitles=[{"timestamp_ms": 0, "text": "Start"}],
            playing_guide=[
                {
                    "step": 1,
                    "title": "Step 1",
                    "description": "Desc",
                    "start_time": "0:00",
                    "end_time": "0:30",
                }
            ],
            sync_offset=0,
            time_created=now,
            time_updated=now,
        ),
        Lesson(
            id=202,
            title="Session 2",
            artist_id=session_artist.id,
            lecture_id=session_lecture.id,
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
    ]
    async with test_session.begin():
        for lesson in lessons:
            test_session.add(lesson)
        await test_session.flush()
    await test_session.commit()
    return lessons


@pytest.fixture
async def session_ticket_usage(
    test_user, session_lecture: Lecture, test_session: AsyncSession
) -> TicketUsage:
    ticket_usage = TicketUsage(
        user_id=test_user.id,
        lecture_id=session_lecture.id,
        used_at=datetime.datetime.now(datetime.timezone.utc),
    )
    async with test_session.begin():
        test_session.add(ticket_usage)
        await test_session.flush()
    await test_session.commit()
    return ticket_usage


@pytest.fixture
async def session_personal_subscription(test_session: AsyncSession) -> Subscription:
    subscription = Subscription(
        id=uuid.uuid4(),
        name="personal",
        is_active=True,
    )
    async with test_session.begin():
        test_session.add(subscription)
        await test_session.flush()
    await test_session.commit()
    return subscription


@pytest.fixture
async def session_user_with_personal(
    user_manager_stub, test_session: AsyncSession, session_personal_subscription
) -> User:
    from fastapi_users.schemas import BaseUserCreate
    from sqlalchemy.orm import selectinload

    user_create = BaseUserCreate(
        email="session_personal@test.com",
        password="password",
        is_superuser=False,
        is_active=True,
    )
    user = await user_manager_stub.create(user_create)
    user.subscription_id = session_personal_subscription.id
    user.expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=30
    )
    async with test_session.begin():
        test_session.add(user)
        await test_session.flush()
    await test_session.commit()

    from app.db.tables import User as UserTable

    async with test_session.begin():
        result = await test_session.execute(
            selectinload(UserTable.subscription)
            if False
            else test_session.get_bind()
            .execute(
                f"SELECT * FROM user WHERE id = '{user.id}'"
            )
        )
    return user


async def test_sut_returns_401_when_unauthenticated(
    client: AsyncClient, session_lessons: list[Lesson]
):
    response = await client.get("/session/201")
    assert response.status_code == 401


async def test_sut_returns_404_when_session_not_found(authorized_client: AsyncClient):
    response = await authorized_client.get("/session/9999")
    assert response.status_code == 404


async def test_sut_returns_403_when_no_ticket_access(
    authorized_client: AsyncClient, session_lessons: list[Lesson]
):
    response = await authorized_client.get("/session/201")
    assert response.status_code == 403


async def test_sut_returns_session_detail_with_valid_ticket(
    authorized_client: AsyncClient,
    session_lessons: list[Lesson],
    session_ticket_usage: TicketUsage,
):
    response = await authorized_client.get("/session/201")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 201
    assert data["title"] == "Session 1"
    assert data["session_type"] == "PLAY"
    assert data["session_type_label"] == "연주 강의"
    assert data["lecture"]["id"] == 200
    assert data["lecture"]["title"] == "Session Test Lecture"
    assert data["lecture"]["total_sessions"] == 2
    assert data["navigation"]["prev_session_id"] is None
    assert data["navigation"]["next_session_id"] == 202


async def test_sut_returns_session_detail_with_subtitles_and_guide(
    authorized_client: AsyncClient,
    session_lessons: list[Lesson],
    session_ticket_usage: TicketUsage,
):
    response = await authorized_client.get("/session/201")
    assert response.status_code == 200

    data = response.json()
    assert len(data["subtitles"]) == 1
    assert data["subtitles"][0]["timestamp_ms"] == 0
    assert data["subtitles"][0]["text"] == "Start"
    assert len(data["playing_guide"]) == 1
    assert data["playing_guide"][0]["step"] == 1
