import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def one_lecture(test_session: AsyncSession) -> None:
    now = datetime.datetime.now()
    async with test_session.begin():
        test_session.add(
            Lecture(
                id=1, artist_id=None, thumbnail=None, title="L", description="d",
                tags=None, length_sec=0, time_created=now, time_updated=now,
            )
        )
    await test_session.commit()


async def test_create_lesson(authorized_client_admin: AsyncClient, one_lecture):
    body = {
        "lecture_id": 1,
        "title": "lesson A",
        "session_type": "PLAY",
        "lecture_ordering": 0,
        "length_sec": 120,
        "text": "intro",
    }
    response = await authorized_client_admin.post("/lesson", json=body)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["id"] > 0
    assert data["title"] == "lesson A"


async def test_create_lesson_forbidden_for_artist(
    authorized_client_artist: AsyncClient, one_lecture
):
    response = await authorized_client_artist.post(
        "/lesson", json={"lecture_id": 1, "title": "x", "length_sec": 0}
    )
    assert response.status_code == 403


async def test_patch_lesson_subtitles(
    authorized_client_admin: AsyncClient, one_lecture
):
    created = await authorized_client_admin.post(
        "/lesson",
        json={"lecture_id": 1, "title": "L", "length_sec": 0},
    )
    lesson_id = created.json()["data"]["id"]
    subtitles = [{"timestamp_ms": 0, "text": "hi"}, {"timestamp_ms": 1000, "text": "yo"}]
    response = await authorized_client_admin.patch(
        f"/lesson/{lesson_id}", json={"subtitles": subtitles}
    )
    assert response.status_code == 200
    assert response.json()["data"]["subtitles"] == subtitles
