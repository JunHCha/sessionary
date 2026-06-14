import abc

from app.video.models import VideoURLResponse


class VideoProvider(abc.ABC):
    @abc.abstractmethod
    async def get_video_url(self, video_id: str) -> VideoURLResponse:
        """비디오 접근 URL 반환"""
        raise NotImplementedError

    @abc.abstractmethod
    async def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        """업로드 후 저장 object key 반환"""
        raise NotImplementedError
