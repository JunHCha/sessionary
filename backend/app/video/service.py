import abc

from app.video.models import VideoURLResponse


class VideoProvider(abc.ABC):
    @abc.abstractmethod
    async def get_video_url(self, video_id: str) -> VideoURLResponse:
        """비디오 접근 URL 반환"""
        raise NotImplementedError
