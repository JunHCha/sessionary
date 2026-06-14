import pytest

from app.sheetmusic.mock import MockSheetmusicProvider
from app.video.mock import MockVideoProvider

pytest_plugins = ["tests.conftest"]


async def test_mock_video_upload_returns_object_key():
    provider = MockVideoProvider()
    key = await provider.upload("clip.mp4", b"data", "video/mp4")
    assert key == "clip.mp4"


async def test_mock_sheetmusic_upload_returns_object_key():
    provider = MockSheetmusicProvider()
    key = await provider.upload("tab.musicxml", b"<xml/>", "application/xml")
    assert key == "tab.musicxml"
