import datetime
from datetime import timedelta

from app.video.models import VideoURLResponse
from app.video.service import VideoProvider


class CloudflareVideoProvider(VideoProvider):
    def __init__(self, account_id: str, api_token: str, subdomain: str | None = None):
        self.account_id = account_id
        self.api_token = api_token
        self.subdomain = subdomain or account_id

    async def get_video_url(self, video_id: str) -> VideoURLResponse:
        signed_token = self._generate_signed_token(video_id)
        expires_at = datetime.datetime.utcnow() + timedelta(hours=2)
        return VideoURLResponse(
            url=f"https://customer-{self.subdomain}.cloudflarestream.com/{video_id}/manifest/video.m3u8?token={signed_token}",
            type="hls",
            expires_at=expires_at,
        )

    def _generate_signed_token(self, video_id: str) -> str:
        raise NotImplementedError("Cloudflare signed token generation not implemented yet")
