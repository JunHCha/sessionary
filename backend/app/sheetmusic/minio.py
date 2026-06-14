import datetime
import io
from datetime import timedelta, timezone

from minio import Minio
from minio.error import S3Error

from app.sheetmusic.models import SheetmusicURLResponse
from app.sheetmusic.service import SheetmusicProvider


class MinIOSheetmusicProvider(SheetmusicProvider):
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str = "sheetmusic",
        secure: bool = False,
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket_name = bucket_name

    async def get_url(self, object_name: str) -> SheetmusicURLResponse:
        expires = timedelta(hours=2)
        try:
            presigned_url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                expires=expires,
            )
        except S3Error as e:
            raise ValueError(f"Failed to generate presigned URL: {e}")

        expires_at = datetime.datetime.now(timezone.utc) + expires
        return SheetmusicURLResponse(
            url=presigned_url,
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
