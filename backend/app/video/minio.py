import datetime
from datetime import timedelta, timezone
import io

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
        public_endpoint: str = "",
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        # presigned URL은 브라우저에서 직접 접근하므로 외부에서 도달 가능한
        # public endpoint로 서명을 생성한다(서명이 host에 묶여 단순 치환 불가).
        # 미지정 시 내부 endpoint를 그대로 사용한다.
        # region을 명시해 minio-py가 서명 전 endpoint로 보내는 GetBucketLocation
        # 네트워크 호출을 건너뛴다(public endpoint는 서버에서 도달 불가).
        self.presign_client = (
            Minio(
                endpoint=public_endpoint,
                access_key=access_key,
                secret_key=secret_key,
                secure=secure,
                region="us-east-1",
            )
            if public_endpoint
            else self.client
        )
        self.bucket_name = bucket_name

    async def get_video_url(self, video_id: str) -> VideoURLResponse:
        expires = timedelta(hours=2)
        try:
            presigned_url = self.presign_client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=video_id,
                expires=expires,
            )
        except S3Error as e:
            raise ValueError(f"Failed to generate presigned URL: {e}")

        expires_at = datetime.datetime.now(timezone.utc) + expires
        return VideoURLResponse(
            url=presigned_url,
            type="direct",
            expires_at=expires_at,
        )

    async def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=io.BytesIO(data),
            length=len(data),
            content_type=content_type,
        )
        return object_name
