import pytest

from app.session.models import SessionType, Subtitle, PlayingGuideStep


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
