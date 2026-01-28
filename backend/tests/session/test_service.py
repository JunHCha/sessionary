import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.db import tables as tb
from app.session.models import SessionType, SessionDetailResponse
from app.session.service import SessionService
from app.video.models import VideoURLResponse


@pytest.fixture
def mock_session_repository():
    return AsyncMock()


@pytest.fixture
def mock_video_provider():
    return AsyncMock()


@pytest.fixture
def session_service(mock_session_repository, mock_video_provider):
    return SessionService(
        repository=mock_session_repository,
        video_provider=mock_video_provider,
    )


def create_mock_lesson(
    id: int = 1,
    title: str = "Test Session",
    session_type: SessionType | None = SessionType.PLAY,
    lecture_ordering: int = 1,
    length_sec: int = 100,
    video_url: str = "video.mp4",
    sheetmusic_url: str = "sheet.gp",
    subtitles: list | None = None,
    playing_guide: list | None = None,
    sync_offset: int = 0,
    lecture_id: int = 10,
    lecture_title: str = "Test Lecture",
) -> tb.Lesson:
    lesson = MagicMock(spec=tb.Lesson)
    lesson.id = id
    lesson.title = title
    lesson.session_type = session_type
    lesson.lecture_ordering = lecture_ordering
    lesson.length_sec = length_sec
    lesson.video_url = video_url
    lesson.sheetmusic_url = sheetmusic_url
    lesson.subtitles = subtitles
    lesson.playing_guide = playing_guide
    lesson.sync_offset = sync_offset
    lesson.lecture_id = lecture_id

    lecture = MagicMock(spec=tb.Lecture)
    lecture.id = lecture_id
    lecture.title = lecture_title
    lesson.lecture = lecture

    return lesson


class TestSessionService:
    async def test_sut_get_session_detail_returns_response_with_video(
        self, session_service, mock_session_repository, mock_video_provider
    ):
        lesson = create_mock_lesson()
        mock_session_repository.get_session_detail.return_value = lesson
        mock_session_repository.get_adjacent_sessions.return_value = (None, 2)
        mock_session_repository.count_sessions_in_lecture.return_value = 5
        mock_video_provider.get_video_url.return_value = VideoURLResponse(
            url="https://signed.url/video.m3u8",
            type="hls",
            expires_at=datetime.datetime.now(datetime.timezone.utc),
        )

        result = await session_service.get_session_detail(1)

        assert isinstance(result, SessionDetailResponse)
        assert result.id == 1
        assert result.title == "Test Session"
        assert result.session_type == SessionType.PLAY
        assert result.session_type_label == "연주 강의"
        assert result.video is not None
        assert result.video.url == "https://signed.url/video.m3u8"

    async def test_sut_get_session_detail_returns_none_when_not_found(
        self, session_service, mock_session_repository
    ):
        mock_session_repository.get_session_detail.return_value = None

        result = await session_service.get_session_detail(9999)

        assert result is None

    async def test_sut_get_session_detail_handles_null_session_type(
        self, session_service, mock_session_repository, mock_video_provider
    ):
        lesson = create_mock_lesson(session_type=None)
        mock_session_repository.get_session_detail.return_value = lesson
        mock_session_repository.get_adjacent_sessions.return_value = (None, None)
        mock_session_repository.count_sessions_in_lecture.return_value = 1
        mock_video_provider.get_video_url.return_value = VideoURLResponse(
            url="https://signed.url/video.m3u8",
            type="hls",
            expires_at=datetime.datetime.now(datetime.timezone.utc),
        )

        result = await session_service.get_session_detail(1)

        assert result.session_type == SessionType.PLAY
        assert result.session_type_label == "연주 강의"

    async def test_sut_get_session_detail_handles_null_video_url(
        self, session_service, mock_session_repository, mock_video_provider
    ):
        lesson = create_mock_lesson(video_url="")
        mock_session_repository.get_session_detail.return_value = lesson
        mock_session_repository.get_adjacent_sessions.return_value = (None, None)
        mock_session_repository.count_sessions_in_lecture.return_value = 1

        result = await session_service.get_session_detail(1)

        assert result.video is None
        mock_video_provider.get_video_url.assert_not_called()

    async def test_sut_get_session_detail_converts_null_subtitles_to_empty_list(
        self, session_service, mock_session_repository, mock_video_provider
    ):
        lesson = create_mock_lesson(subtitles=None)
        mock_session_repository.get_session_detail.return_value = lesson
        mock_session_repository.get_adjacent_sessions.return_value = (None, None)
        mock_session_repository.count_sessions_in_lecture.return_value = 1
        mock_video_provider.get_video_url.return_value = VideoURLResponse(
            url="https://signed.url/video.m3u8",
            type="hls",
            expires_at=datetime.datetime.now(datetime.timezone.utc),
        )

        result = await session_service.get_session_detail(1)

        assert result.subtitles == []

    async def test_sut_get_session_detail_converts_null_playing_guide_to_empty_list(
        self, session_service, mock_session_repository, mock_video_provider
    ):
        lesson = create_mock_lesson(playing_guide=None)
        mock_session_repository.get_session_detail.return_value = lesson
        mock_session_repository.get_adjacent_sessions.return_value = (None, None)
        mock_session_repository.count_sessions_in_lecture.return_value = 1
        mock_video_provider.get_video_url.return_value = VideoURLResponse(
            url="https://signed.url/video.m3u8",
            type="hls",
            expires_at=datetime.datetime.now(datetime.timezone.utc),
        )

        result = await session_service.get_session_detail(1)

        assert result.playing_guide == []

    async def test_sut_get_session_detail_includes_navigation(
        self, session_service, mock_session_repository, mock_video_provider
    ):
        lesson = create_mock_lesson()
        mock_session_repository.get_session_detail.return_value = lesson
        mock_session_repository.get_adjacent_sessions.return_value = (5, 7)
        mock_session_repository.count_sessions_in_lecture.return_value = 10
        mock_video_provider.get_video_url.return_value = VideoURLResponse(
            url="https://signed.url/video.m3u8",
            type="hls",
            expires_at=datetime.datetime.now(datetime.timezone.utc),
        )

        result = await session_service.get_session_detail(6)

        assert result.navigation.prev_session_id == 5
        assert result.navigation.next_session_id == 7
