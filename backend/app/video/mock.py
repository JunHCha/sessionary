import datetime

from app.video.models import VideoURLResponse
from app.video.service import VideoProvider


class MockVideoProvider(VideoProvider):
    async def get_video_url(self, video_id: str) -> VideoURLResponse:
        return VideoURLResponse(
            url=f"https://mock.example.com/{video_id}",
            type="hls",
            expires_at=datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=1),
        )

    async def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        return object_name
