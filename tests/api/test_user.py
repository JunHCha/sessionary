import datetime
import uuid

import orjson
import pytest
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import ArtistXLecture, Lecture, Subscription, User, UserXSubscription

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def dummy_users(test_session: AsyncSession) -> None:

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
    lecture_1_1 = Lecture(
        id=11,
        title="lecture1-1",
        description="description1",
        length_sec=0,
        time_created=datetime.datetime.now(),
        time_updated=datetime.datetime.now(),
    )
    lecture_1_2 = Lecture(
        id=12,
        title="lecture1-2",
        description="description1",
        length_sec=0,
        time_created=datetime.datetime.now(),
        time_updated=datetime.datetime.now(),
    )
    artist_lecture_associations = [
        ArtistXLecture(artist_id=artist_1.id, lecture_id=lecture_1_1.id),
        ArtistXLecture(artist_id=artist_1.id, lecture_id=lecture_1_2.id),
    ]
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
    subscription_1 = Subscription(
        id=uuid.uuid4(), expires_at=datetime.datetime.now() + datetime.timedelta(days=1)
    )
    user_x_subscription_1 = UserXSubscription(
        user_id=user_1.id, subscription_id=subscription_1.id
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
        test_session.add_all(
            [artist_1, artist_2, user_1, admin_1, lecture_1_1, lecture_1_2]
        )
    await test_session.commit()
    async with test_session.begin():
        test_session.add_all(
            artist_lecture_associations + [subscription_1, user_x_subscription_1]
        )
    await test_session.commit()


async def test_sut_create_subscription_when_register_user(test_user):
    # then
    assert test_user.subscription is not None
    assert test_user.subscription.is_active is True
    assert test_user.subscription.name == "ticket"


async def test_sut_create_auth_session_when_login(
    client: AsyncClient, auth_redis: Redis, test_user
) -> None:

    # when
    response = await client.post(
        "/user/auth/login",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"username": "test@test.com", "password": "password"},
    )

    # then
    assert response.status_code == 200

    token = response.json().get("access_token")
    session = await auth_redis.get(f"auth-session-id:{token}")
    assert orjson.loads(session).get("email") == "test@test.com"


async def test_sut_fetch_artists(client: AsyncClient, dummy_users) -> None:
    # when
    response = await client.get("/user/artists")

    # then
    assert response.status_code == 200
    content = response.json()
    assert len(content.get("data")) == 2
    assert {user.get("nickname") for user in content.get("data")} == {
        "artist1",
        "artist2",
    }
    assert len(content.get("data")[0].get("lectures")) == 2


async def test_sut_get_me(authorized_client: AsyncClient) -> None:
    # when
    response = await authorized_client.get("/user/me")

    # then
    assert response.status_code == 200
    content = response.json()
    assert content.get("email") == "test@test.com"
    assert content.get("is_superuser") is False
