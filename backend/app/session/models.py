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
