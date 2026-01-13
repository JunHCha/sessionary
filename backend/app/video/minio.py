import datetime
from datetime import timedelta

from minio import Minio
from minio.error import S3Error

from app.video.models import VideoURLResponse
from app.video.service import VideoProvider


class MinIOVideoProvider(VideoProvider):
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str = "videos",
        secure: bool = False,
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket_name = bucket_name

    async def get_video_url(self, video_id: str) -> VideoURLResponse:
        expires = timedelta(hours=2)
        try:
            presigned_url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=video_id,
                expires=expires,
            )
        except S3Error as e:
            raise ValueError(f"Failed to generate presigned URL: {e}")

        expires_at = datetime.datetime.utcnow() + expires
        return VideoURLResponse(
            url=presigned_url,
            type="direct",
            expires_at=expires_at,
        )
