import datetime
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import ArtistXLecture, Lecture, User

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
        test_session.add_all(artist_lecture_associations)
    await test_session.commit()


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


async def test_sut_get_me(test_user, authorized_client: AsyncClient) -> None:
    # when
    response = await authorized_client.get("/user/me")

    # then
    assert response.status_code == 200
    content = response.json()
    assert content.get("nickname") == "test"
    assert content.get("is_superuser") is False
