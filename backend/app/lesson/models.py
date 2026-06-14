import datetime

from app.core.models import BaseModel, BaseSchema
from app.session.models import PlayingGuideStep, SessionType, Subtitle


class LessonInLecture(BaseModel):
    id: int
    title: str
    length_sec: int
    lecture_ordering: int
    time_created: datetime.datetime
    time_updated: datetime.datetime


class LessonAdminDetail(BaseModel):
    id: int
    lecture_id: int
    title: str
    length_sec: int
    text: str | None
    lecture_ordering: int
    session_type: SessionType | None
    sheetmusic_url: str | None
    video_url: str | None
    sync_offset: int
    subtitles: list[Subtitle]
    playing_guide: list[PlayingGuideStep]


class LessonAdminSchema(BaseSchema):
    data: LessonAdminDetail


class CreateLessonBody(BaseSchema):
    lecture_id: int
    title: str
    length_sec: int = 0
    text: str = ""
    lecture_ordering: int = 0
    session_type: SessionType | None = None
    sync_offset: int = 0
    subtitles: list[Subtitle] = []
    playing_guide: list[PlayingGuideStep] = []


class UpdateLessonBody(BaseSchema):
    title: str | None = None
    length_sec: int | None = None
    text: str | None = None
    lecture_ordering: int | None = None
    session_type: SessionType | None = None
    sync_offset: int | None = None
    subtitles: list[Subtitle] | None = None
    playing_guide: list[PlayingGuideStep] | None = None
