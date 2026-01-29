from app.session.models import (
    LectureInfo,
    PlayingGuideStep,
    SessionDetailResponse,
    SessionNavigation,
    SessionType,
    Subtitle,
    VideoInfo,
)
from app.session.repository import BaseSessionRepository
from app.video.service import VideoProvider


class SessionService:
    def __init__(
        self, repository: BaseSessionRepository, video_provider: VideoProvider
    ) -> None:
        self.repository = repository
        self.video_provider = video_provider

    async def get_session_detail(self, session_id: int) -> SessionDetailResponse | None:
        lesson = await self.repository.get_session_detail(session_id)
        if lesson is None:
            return None

        session_type = lesson.session_type or SessionType.PLAY

        video_info = None
        if lesson.video_url:
            video_response = await self.video_provider.get_video_url(lesson.video_url)
            video_info = VideoInfo(
                url=video_response.url,
                type=video_response.type,
                expires_at=video_response.expires_at,
            )

        prev_id, next_id = await self.repository.get_adjacent_sessions(
            session_id, lesson.lecture_id
        )
        total_sessions = await self.repository.count_sessions_in_lecture(
            lesson.lecture_id
        )

        subtitles_data = lesson.subtitles or []
        subtitles = [Subtitle(**s) for s in subtitles_data]

        playing_guide_data = lesson.playing_guide or []
        playing_guide = [PlayingGuideStep(**g) for g in playing_guide_data]

        return SessionDetailResponse(
            id=lesson.id,
            title=lesson.title,
            session_type=session_type,
            session_type_label=session_type.label,
            lecture_ordering=lesson.lecture_ordering,
            length_sec=lesson.length_sec,
            lecture=LectureInfo(
                id=lesson.lecture.id,
                title=lesson.lecture.title,
                total_sessions=total_sessions,
            ),
            video=video_info,
            sheetmusic_url=lesson.sheetmusic_url or None,
            sync_offset=lesson.sync_offset,
            subtitles=subtitles,
            playing_guide=playing_guide,
            navigation=SessionNavigation(
                prev_session_id=prev_id,
                next_session_id=next_id,
            ),
        )
