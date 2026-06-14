import datetime

from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def lectures(test_session: AsyncSession) -> None:
    now = datetime.datetime.now()
    async with test_session.begin():
        test_session.add_all([
            Lecture(id=i, artist_id=None, thumbnail=None, title=f"L{i}",
                    description="d", tags=None, length_sec=0,
                    time_created=now, time_updated=now)
            for i in (1, 2, 3)
        ])
    await test_session.commit()


async def test_put_and_get_curation(
    authorized_client_admin: AsyncClient, client: AsyncClient, lectures
):
    put = await authorized_client_admin.put(
        "/curation/TRENDING", json={"lecture_ids": [3, 1]}
    )
    assert put.status_code == 200

    get = await client.get("/curation")
    assert get.status_code == 200
    data = get.json()["data"]
    assert [item["id"] for item in data["TRENDING"]] == [3, 1]
    assert data["NEW"] == []


async def test_put_curation_forbidden_for_non_admin(
    authorized_client_artist: AsyncClient, lectures
):
    response = await authorized_client_artist.put(
        "/curation/NEW", json={"lecture_ids": [1]}
    )
    assert response.status_code == 403
