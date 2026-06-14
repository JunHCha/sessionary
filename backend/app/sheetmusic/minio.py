import datetime
from datetime import timedelta, timezone
import io

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
        public_endpoint: str = "",
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        # presigned URL은 브라우저에서 직접 접근하므로 외부에서 도달 가능한
        # public endpoint로 서명을 생성한다. 미지정 시 내부 endpoint 사용.
        # region을 명시해 서명 전 GetBucketLocation 네트워크 호출을 건너뛴다.
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

    async def get_url(self, object_name: str) -> SheetmusicURLResponse:
        expires = timedelta(hours=2)
        try:
            presigned_url = self.presign_client.presigned_get_object(
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
