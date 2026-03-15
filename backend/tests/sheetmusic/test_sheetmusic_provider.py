import datetime
from unittest.mock import MagicMock, patch

import pytest
from minio.error import S3Error

from app.sheetmusic.models import SheetmusicURLResponse
from app.sheetmusic.mock import MockSheetmusicProvider
from app.sheetmusic.minio import MinIOSheetmusicProvider


class TestMockSheetmusicProvider:
    async def test_sut_get_url_returns_presigned_response(self):
        provider = MockSheetmusicProvider()

        result = await provider.get_url("sheet.gp")

        assert isinstance(result, SheetmusicURLResponse)
        assert "sheet.gp" in result.url
        assert result.expires_at > datetime.datetime.now(datetime.timezone.utc)

    async def test_sut_get_url_returns_different_urls_for_different_keys(self):
        provider = MockSheetmusicProvider()

        result_a = await provider.get_url("a.gp")
        result_b = await provider.get_url("b.gp")

        assert result_a.url != result_b.url


class TestMinIOSheetmusicProvider:
    @pytest.fixture
    def mock_minio_client(self):
        with patch("app.sheetmusic.minio.Minio") as mock_cls:
            client = MagicMock()
            mock_cls.return_value = client
            yield client

    @pytest.fixture
    def provider(self, mock_minio_client):
        return MinIOSheetmusicProvider(
            endpoint="localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            bucket_name="sheetmusic",
        )

    async def test_sut_get_url_returns_presigned_url(
        self, provider, mock_minio_client
    ):
        mock_minio_client.presigned_get_object.return_value = (
            "https://minio.local/sheetmusic/sheet.gp?signature=abc"
        )

        result = await provider.get_url("sheet.gp")

        assert isinstance(result, SheetmusicURLResponse)
        assert "sheet.gp" in result.url
        assert result.expires_at > datetime.datetime.now(datetime.timezone.utc)
        mock_minio_client.presigned_get_object.assert_called_once()

    async def test_sut_get_url_raises_on_s3_error(
        self, provider, mock_minio_client
    ):
        mock_minio_client.presigned_get_object.side_effect = S3Error(
            "NoSuchKey", "Object not found", "", "", "", ""
        )

        with pytest.raises(ValueError, match="Failed to generate presigned URL"):
            await provider.get_url("missing.gp")
