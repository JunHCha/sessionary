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


async def test_report_position_returns_extended_progress(
    authorized_client: AsyncClient,
    lecture_with_lessons: tb.Lecture,
):
    response = await authorized_client.put(
        "/progress/lesson/701/position",
        json={"position_sec": 30, "duration_sec": 60},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 3
    assert data["resume_lesson_id"] == 700
    assert data["resume_position_sec"] == 0
    by_lesson = {item["lesson_id"]: item for item in data["lessons"]}
    assert by_lesson[701]["percent"] == 50
    assert by_lesson[701]["last_position_sec"] == 30
    assert by_lesson[701]["completed"] is False


async def test_report_position_requires_auth(
    client: AsyncClient,
    lecture_with_lessons: tb.Lecture,
):
    response = await client.put(
        "/progress/lesson/701/position",
        json={"position_sec": 30, "duration_sec": 60},
    )
    assert response.status_code == 401
