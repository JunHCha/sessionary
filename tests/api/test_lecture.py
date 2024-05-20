import datetime
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import ArtistXLecture, Lecture, LectureXLesson, Lesson, User


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
            time_created=now + datetime.timedelta(hours=num - 10),
            time_updated=now + datetime.timedelta(hours=num - 10),
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
            time_created=now,
            time_updated=now,
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
            time_created=now + datetime.timedelta(hours=1),
            time_updated=now + datetime.timedelta(hours=1),
        )
        for num in range(15, 20)
    ]
    lessons_ordering = [
        LectureXLesson(lecture_id=10, lesson_id=num, ordering=num - 9)
        for num in range(10, 15)
    ] + [
        LectureXLesson(lecture_id=11, lesson_id=num, ordering=num - 9)
        for num in range(15, 20)
    ]
    artists_in_lectures = [
        ArtistXLecture(artist_id=artist_1.id, lecture_id=10),
        ArtistXLecture(artist_id=artist_2.id, lecture_id=11),
    ]

    async with test_session.begin():
        test_session.add_all([artist_1, artist_2] + lectures)
        await test_session.flush()
        test_session.add_all(lessons + artists_in_lectures)
        await test_session.flush()
        test_session.add_all(lessons_ordering)
    await test_session.commit()


async def test_sut_fetch_recommended_lectures(client: AsyncClient, dummy_lectures):
    # when
    response = await client.get("/lecture?page=1&per_page=20")

    # then
    assert response.status_code == 200

    content = response.json()
    assert len(content["data"]) == 20
    assert all(
        content["data"][index]["time_updated"]
        > content["data"][index + 1]["time_updated"]
        for index in range(9)
    )
    assert content["meta"] == {
        "total_items": 100,
        "total_pages": 5,
        "curr_page": 1,
        "per_page": 20,
    }


async def test_sut_fetch_lecture_datail(client: AsyncClient, dummy_lectures):
    # when
    response = await client.get("/lecture/10")

    # then
    assert response.status_code == 200
    content = response.json()
    assert content["data"]["id"] == 10
    assert content["data"]["title"] == "lecture1"
    assert content["data"]["description"] == "description1"
    assert [lesson["title"] for lesson in content["data"]["lessons"]] == [
        f"lesson1-{num - 9}" for num in range(10, 15)
    ]


async def test_sut_create_lecture(authorized_client_artist: AsyncClient):
    # given
    body = {
        "title": "new lecture",
        "description": "new lecture description",
    }

    # when
    response = await authorized_client_artist.post("/lecture", json=body)

    # then
    assert response.status_code == 201
    content = response.json()
    assert content["data"]["title"] == "new lecture"
    assert content["data"]["description"] == "new lecture description"
    assert content["data"]["lessons"] == []


async def test_sut_raise_403_if_nonartist_user_try_to_create_lecture(
    client: AsyncClient, dummy_lectures
):
    # given
    body = {
        "title": "new lecture",
        "description": "new lecture description",
    }

    # when
    response = await client.post("/lecture", json=body)

    # then
    assert response.status_code == 401
