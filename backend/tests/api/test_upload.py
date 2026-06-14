import datetime
import uuid

from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture, Lesson, User

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def lecture_and_lesson(test_session: AsyncSession) -> None:
    now = datetime.datetime.now()
    artist = User(
        id=uuid.uuid4(), subscription_id=None, time_created=now, time_updated=now,
        email="a@a.com", nickname="a", hashed_password="p",
        is_artist=True, is_superuser=False, is_active=True,
    )
    async with test_session.begin():
        test_session.add(artist)
        await test_session.flush()
        test_session.add(
            Lecture(id=1, artist_id=None, thumbnail=None, title="L", description="d",
                    tags=None, length_sec=0, time_created=now, time_updated=now)
        )
        await test_session.flush()
        test_session.add(
            Lesson(id=1, title="L", artist_id=artist.id, lecture_id=1,
                   sheetmusic_url="", video_url="", text="", length_sec=0,
                   lecture_ordering=0, time_created=now, time_updated=now)
        )
    await test_session.commit()


def _multipart_client(client: AsyncClient) -> AsyncClient:
    """기본 JSON Content-Type 헤더를 제거해 httpx가 multipart 경계를 설정하도록 한다."""
    client.headers.pop("Content-Type", None)
    return client


async def test_upload_lesson_video(authorized_client_admin: AsyncClient, lecture_and_lesson):
    client = _multipart_client(authorized_client_admin)
    files = {"file": ("clip.mp4", b"binarydata", "video/mp4")}
    response = await client.post("/lesson/1/video", files=files)
    assert response.status_code == 200
    assert response.json()["data"]["video_url"]


async def test_upload_lesson_sheetmusic(authorized_client_admin: AsyncClient, lecture_and_lesson):
    client = _multipart_client(authorized_client_admin)
    files = {"file": ("tab.musicxml", b"<score/>", "application/xml")}
    response = await client.post("/lesson/1/sheetmusic", files=files)
    assert response.status_code == 200
    assert response.json()["data"]["sheetmusic_url"]


async def test_upload_video_forbidden_for_artist(authorized_client_artist: AsyncClient, lecture_and_lesson):
    client = _multipart_client(authorized_client_artist)
    files = {"file": ("clip.mp4", b"x", "video/mp4")}
    response = await client.post("/lesson/1/video", files=files)
    assert response.status_code == 403
