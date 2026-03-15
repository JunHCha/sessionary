import datetime

import pytest

from app.sheetmusic.models import SheetmusicURLResponse
from app.sheetmusic.mock import MockSheetmusicProvider


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
