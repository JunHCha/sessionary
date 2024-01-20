import datetime
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def dummy_users(test_session: AsyncSession) -> None:
    from app.db.tables import User

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
    user_1 = User(
        id=uuid.uuid4(),
        subscription_id=None,
        time_created=now,
        time_updated=now,
        email="user1@test.com",
        nickname="user1",
        hashed_password="password",
        is_artist=False,
        is_superuser=False,
        is_active=True,
    )
    admin_1 = User(
        id=uuid.uuid4(),
        subscription_id=None,
        time_created=now,
        time_updated=now,
        email="admin1@test.com",
        nickname="admin1",
        hashed_password="password",
        is_artist=False,
        is_superuser=True,
        is_active=True,
    )
    async with test_session.begin():
        test_session.add_all([artist_1, artist_2, user_1, admin_1])


async def test_fetch_artists(client: AsyncClient, dummy_users) -> None:
    # when
    response = await client.get("/api/user/artists")

    # then
    assert response.status_code == 200
    content = response.json()
    assert len(content.get("data")) == 2
    assert {user.get("nickname") for user in content.get("data")} == {
        "artist1",
        "artist2",
    }


async def test_get_me(authorized_client: AsyncClient, test_user) -> None:
    # when
    response = await authorized_client.get("/api/user/me")

    # then
    assert response.status_code == 200
    content = response.json()
    assert content.get("nickname") == "test"
    assert content.get("is_superuser") is False
    assert content.get("time_created") is not None
    assert content.get("lectures") == []
    assert content.get("lessons") == []
