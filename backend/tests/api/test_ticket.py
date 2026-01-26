import datetime
import uuid

from httpx import AsyncClient
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture, Subscription, TicketUsage, User

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def dummy_lecture(test_session: AsyncSession) -> Lecture:
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
    lecture = Lecture(
        id=10,
        artist_id=artist.id,
        thumbnail="thumbnails1.png",
        title="lecture1",
        description="description1",
        tags=("원곡카피", "Easy"),
        length_sec=0,
        time_created=now,
        time_updated=now,
    )

    async with test_session.begin():
        test_session.add(artist)
        test_session.add(lecture)
        await test_session.flush()
    await test_session.commit()
    return lecture


@pytest.fixture
async def personal_subscription(test_session: AsyncSession) -> Subscription:
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
async def test_user_with_personal(
    user_manager_stub, test_session: AsyncSession, personal_subscription: Subscription
) -> User:
    from fastapi_users.schemas import BaseUserCreate
    from sqlalchemy.orm import selectinload

    user_create = BaseUserCreate(
        email="personal@test.com",
        password="password",
        is_superuser=False,
        is_active=True,
    )
    user = await user_manager_stub.create(user_create)
    user.subscription_id = personal_subscription.id
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
            select(UserTable)
            .options(selectinload(UserTable.subscription))
            .where(UserTable.id == user.id)
        )
        user_with_subscription = result.scalar_one()
    return user_with_subscription


@pytest.fixture
async def used_ticket(
    test_user: User, dummy_lecture: Lecture, test_session: AsyncSession
) -> TicketUsage:
    ticket_usage = TicketUsage(
        user_id=test_user.id,
        lecture_id=dummy_lecture.id,
        used_at=datetime.datetime.now(datetime.timezone.utc),
    )
    async with test_session.begin():
        test_session.add(ticket_usage)
        await test_session.flush()
    await test_session.commit()
    return ticket_usage


@pytest.fixture
def make_authorized_client_personal(
    make_authorized_client, test_user_with_personal, test_session: AsyncSession
):
    async def _make_client():
        return await make_authorized_client(
            test_user_with_personal, test_session, token="SESSIONTOKEN_PERSONAL"
        )

    return _make_client


@pytest.fixture
async def authorized_client_personal(
    make_authorized_client_personal,
) -> AsyncClient:
    return await make_authorized_client_personal()


async def test_sut_returns_401_when_unauthenticated(
    client: AsyncClient, dummy_lecture: Lecture
):
    response = await client.get(f"/ticket/lecture/{dummy_lecture.id}")
    assert response.status_code == 401


async def test_openapi_spec_includes_401_response_for_get_lecture_access(client: AsyncClient):
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    openapi_spec = response.json()
    path_spec = openapi_spec["paths"]["/ticket/lecture/{lecture_id}"]["get"]
    assert "401" in path_spec["responses"]
    assert path_spec["responses"]["401"]["description"] == "Missing token or inactive user."


async def test_openapi_spec_includes_401_response_for_use_ticket(client: AsyncClient):
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    openapi_spec = response.json()
    path_spec = openapi_spec["paths"]["/ticket/lecture/{lecture_id}"]["post"]
    assert "401" in path_spec["responses"]
    assert path_spec["responses"]["401"]["description"] == "Missing token or inactive user."


async def test_sut_returns_accessible_true_for_unlimited_subscription(
    authorized_client_personal: AsyncClient, dummy_lecture: Lecture
):
    response = await authorized_client_personal.get(
        f"/ticket/lecture/{dummy_lecture.id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["accessible"] is True
    assert data["reason"] == "unlimited"


async def test_sut_returns_accessible_false_when_ticket_not_used(
    authorized_client: AsyncClient, dummy_lecture: Lecture
):
    response = await authorized_client.get(f"/ticket/lecture/{dummy_lecture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["accessible"] is False
    assert data["ticket_count"] == 3
    assert data["reason"] is None


async def test_sut_returns_accessible_true_when_ticket_already_used(
    authorized_client: AsyncClient, dummy_lecture: Lecture, used_ticket: TicketUsage
):
    response = await authorized_client.get(f"/ticket/lecture/{dummy_lecture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["accessible"] is True
    assert data["reason"] == "ticket_used"
    assert data["expires_at"] is not None


async def test_sut_use_ticket_creates_usage_and_decreases_count(
    authorized_client: AsyncClient,
    dummy_lecture: Lecture,
    test_user: User,
    test_session: AsyncSession,
):
    response = await authorized_client.post(f"/ticket/lecture/{dummy_lecture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["accessible"] is True
    assert data["reason"] == "ticket_used"

    from app.db.tables import User as UserTable

    async with test_session.begin():
        result = await test_session.execute(
            select(UserTable).where(UserTable.id == test_user.id)
        )
        refreshed_user = result.scalar_one()
        assert refreshed_user.ticket_count == 2


async def test_sut_use_ticket_fails_when_no_tickets(
    authorized_client: AsyncClient,
    dummy_lecture: Lecture,
    test_user: User,
    test_session: AsyncSession,
):
    test_user.ticket_count = 0
    async with test_session.begin():
        test_session.add(test_user)
        await test_session.flush()
    await test_session.commit()

    response = await authorized_client.post(f"/ticket/lecture/{dummy_lecture.id}")
    assert response.status_code == 403


async def test_sut_use_ticket_returns_existing_when_already_used(
    authorized_client: AsyncClient,
    dummy_lecture: Lecture,
    used_ticket: TicketUsage,
    test_user: User,
    test_session: AsyncSession,
):
    from app.db.tables import User as UserTable

    async with test_session.begin():
        result = await test_session.execute(
            select(UserTable).where(UserTable.id == test_user.id)
        )
        initial_user = result.scalar_one()
        initial_count = initial_user.ticket_count

    response = await authorized_client.post(f"/ticket/lecture/{dummy_lecture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["accessible"] is True
    assert data["reason"] == "ticket_used"

    async with test_session.begin():
        result = await test_session.execute(
            select(UserTable).where(UserTable.id == test_user.id)
        )
        refreshed_user = result.scalar_one()
        assert refreshed_user.ticket_count == initial_count
