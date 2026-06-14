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
                id=1,
                artist_id=None,
                thumbnail=None,
                title="old title",
                description="old desc",
                tags=("원곡카피", "Easy"),
                length_sec=0,
                time_created=now,
                time_updated=now,
            )
        )
    await test_session.commit()


async def test_patch_lecture_updates_fields(
    authorized_client_admin: AsyncClient, one_lecture
):
    body = {
        "title": "new title",
        "description": "new desc",
        "tags": ["해석버전", "Advanced"],
    }
    response = await authorized_client_admin.patch("/lecture/1", json=body)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == "new title"
    assert data["description"] == "new desc"
    assert data["tags"] == ["해석버전", "Advanced"]


async def test_patch_lecture_partial_keeps_other_fields(
    authorized_client_admin: AsyncClient, one_lecture
):
    response = await authorized_client_admin.patch(
        "/lecture/1", json={"title": "only title"}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == "only title"
    assert data["description"] == "old desc"


async def test_patch_lecture_forbidden_for_non_superuser(
    authorized_client_artist: AsyncClient, one_lecture
):
    response = await authorized_client_artist.patch(
        "/lecture/1", json={"title": "x"}
    )
    assert response.status_code == 403
