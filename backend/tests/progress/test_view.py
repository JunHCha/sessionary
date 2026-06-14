from httpx import AsyncClient

from app.db import tables as tb

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


async def test_mark_complete_returns_progress(
    authorized_client: AsyncClient,
    lecture_with_lessons: tb.Lecture,
):
    response = await authorized_client.post("/progress/lesson/700")
    assert response.status_code == 200
    data = response.json()
    assert data["completed_count"] == 1
    assert data["total_count"] == 3
    assert data["percent"] == 33
    assert data["next_lesson_id"] == 701
    assert data["completed_lesson_ids"] == [700]


async def test_mark_complete_requires_auth(
    client: AsyncClient,
    lecture_with_lessons: tb.Lecture,
):
    response = await client.post("/progress/lesson/700")
    assert response.status_code == 401


async def test_mark_complete_is_idempotent(
    authorized_client: AsyncClient,
    lecture_with_lessons: tb.Lecture,
):
    await authorized_client.post("/progress/lesson/700")
    response = await authorized_client.post("/progress/lesson/700")
    assert response.status_code == 200
    assert response.json()["completed_count"] == 1
