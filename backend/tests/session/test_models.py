import datetime

import pytest

from app.session.models import (
    SessionType,
    Subtitle,
    PlayingGuideStep,
    LectureInfo,
    VideoInfo,
    SessionNavigation,
    SessionDetailResponse,
)


class TestSessionType:
    def test_sut_has_all_session_types(self):
        assert SessionType.PLAY.value == "PLAY"
        assert SessionType.TALK.value == "TALK"
        assert SessionType.JAM.value == "JAM"
        assert SessionType.BASIC.value == "BASIC"
        assert SessionType.SHEET.value == "SHEET"

    def test_sut_returns_korean_label(self):
        assert SessionType.PLAY.label == "연주 강의"
        assert SessionType.TALK.label == "곡 해석"
        assert SessionType.JAM.label == "리허설"
        assert SessionType.BASIC.label == "기본기"
        assert SessionType.SHEET.label == "악보"


class TestSubtitle:
    def test_sut_creates_valid_subtitle(self):
        subtitle = Subtitle(timestamp_ms=12000, text="Am 코드에서 시작해서...")
        assert subtitle.timestamp_ms == 12000
        assert subtitle.text == "Am 코드에서 시작해서..."

    def test_sut_rejects_negative_timestamp(self):
        with pytest.raises(ValueError):
            Subtitle(timestamp_ms=-1, text="test")


class TestPlayingGuideStep:
    def test_sut_creates_valid_guide_step(self):
        step = PlayingGuideStep(
            step=1,
            title="코드 포지션 잡기",
            description="Am 코드 형태로 손가락을 배치...",
            start_time="0:00",
            end_time="0:28",
            tip="처음에는 코드를 천천히 잡고...",
        )
        assert step.step == 1
        assert step.title == "코드 포지션 잡기"

    def test_sut_allows_optional_tip(self):
        step = PlayingGuideStep(
            step=1,
            title="코드 포지션 잡기",
            description="Am 코드 형태로 손가락을 배치...",
            start_time="0:00",
            end_time="0:28",
        )
        assert step.tip is None

    def test_sut_rejects_non_positive_step(self):
        with pytest.raises(ValueError):
            PlayingGuideStep(
                step=0,
                title="제목",
                description="설명",
                start_time="0:00",
                end_time="0:28",
            )


class TestSessionDetailResponse:
    def test_sut_creates_valid_response(self):
        response = SessionDetailResponse(
            id=1,
            title="아르페지오 인트로 마스터하기",
            session_type=SessionType.PLAY,
            session_type_label="연주 강의",
            lecture_ordering=2,
            length_sec=168,
            lecture=LectureInfo(id=1, title="Stairway to Heaven", total_sessions=10),
            video=VideoInfo(
                url="https://example.com/video.m3u8",
                type="hls",
                expires_at=datetime.datetime.now(datetime.timezone.utc),
            ),
            sheetmusic_url="https://example.com/sheet.gp",
            sync_offset=0,
            subtitles=[],
            playing_guide=[],
            navigation=SessionNavigation(prev_session_id=None, next_session_id=3),
        )
        assert response.id == 1
        assert response.session_type == SessionType.PLAY
        assert response.session_type_label == "연주 강의"

    def test_sut_allows_null_video(self):
        response = SessionDetailResponse(
            id=1,
            title="악보 세션",
            session_type=SessionType.SHEET,
            session_type_label="악보",
            lecture_ordering=1,
            length_sec=0,
            lecture=LectureInfo(id=1, title="Test Lecture", total_sessions=1),
            video=None,
            sheetmusic_url=None,
            sync_offset=0,
            subtitles=[],
            playing_guide=[],
            navigation=SessionNavigation(prev_session_id=None, next_session_id=None),
        )
        assert response.video is None

    def test_sut_includes_subtitles_and_playing_guide(self):
        response = SessionDetailResponse(
            id=1,
            title="테스트",
            session_type=SessionType.PLAY,
            session_type_label="연주 강의",
            lecture_ordering=1,
            length_sec=100,
            lecture=LectureInfo(id=1, title="Test", total_sessions=1),
            video=None,
            sheetmusic_url=None,
            sync_offset=0,
            subtitles=[Subtitle(timestamp_ms=0, text="시작")],
            playing_guide=[
                PlayingGuideStep(
                    step=1,
                    title="Step 1",
                    description="Description",
                    start_time="0:00",
                    end_time="0:30",
                )
            ],
            navigation=SessionNavigation(prev_session_id=None, next_session_id=None),
        )
        assert len(response.subtitles) == 1
        assert len(response.playing_guide) == 1
