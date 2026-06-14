from httpx import AsyncClient

from app.db import tables as tb

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


async def test_lecture_detail_progress_null_when_anonymous(
    client: AsyncClient,
    lecture_with_lessons: tb.Lecture,
):
    response = await client.get(f"/lecture/{lecture_with_lessons.id}")
    assert response.status_code == 200
    assert response.json()["data"]["progress"] is None


async def test_lecture_detail_progress_present_when_authenticated(
    authorized_client: AsyncClient,
    lecture_with_lessons: tb.Lecture,
):
    response = await authorized_client.get(f"/lecture/{lecture_with_lessons.id}")
    assert response.status_code == 200
    progress = response.json()["data"]["progress"]
    assert progress is not None
    assert progress["completed_count"] == 0
    assert progress["total_count"] == 3
    assert progress["next_lesson_id"] == 700


async def test_lecture_detail_progress_reflects_completion(
    authorized_client: AsyncClient,
    lecture_with_lessons: tb.Lecture,
):
    await authorized_client.post("/progress/lesson/700")
    response = await authorized_client.get(f"/lecture/{lecture_with_lessons.id}")
    progress = response.json()["data"]["progress"]
    assert progress["completed_count"] == 1
    assert progress["completed_lesson_ids"] == [700]
    assert progress["next_lesson_id"] == 701
