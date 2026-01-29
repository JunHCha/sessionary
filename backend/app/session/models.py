import datetime
from enum import Enum

from pydantic import Field

from app.core.models import BaseModel


class SessionType(str, Enum):
    PLAY = "PLAY"
    TALK = "TALK"
    JAM = "JAM"
    BASIC = "BASIC"
    SHEET = "SHEET"

    @property
    def label(self) -> str:
        return {
            "PLAY": "연주 강의",
            "TALK": "곡 해석",
            "JAM": "리허설",
            "BASIC": "기본기",
            "SHEET": "악보",
        }[self.value]


class Subtitle(BaseModel):
    timestamp_ms: int = Field(..., ge=0)
    text: str


class PlayingGuideStep(BaseModel):
    step: int = Field(..., gt=0)
    title: str
    description: str
    start_time: str
    end_time: str
    tip: str | None = None


class LectureInfo(BaseModel):
    id: int
    title: str
    total_sessions: int


class VideoInfo(BaseModel):
    model_config = {"frozen": False}

    url: str
    type: str
    expires_at: "datetime.datetime"


class SessionNavigation(BaseModel):
    prev_session_id: int | None
    next_session_id: int | None


class SessionDetailResponse(BaseModel):
    model_config = {"frozen": False}

    id: int
    title: str
    session_type: SessionType
    session_type_label: str
    lecture_ordering: int
    length_sec: int
    lecture: LectureInfo
    video: VideoInfo | None
    sheetmusic_url: str | None
    sync_offset: int
    subtitles: list[Subtitle]
    playing_guide: list[PlayingGuideStep]
    navigation: SessionNavigation
