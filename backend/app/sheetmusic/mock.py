import datetime

from app.sheetmusic.models import SheetmusicURLResponse
from app.sheetmusic.service import SheetmusicProvider


class MockSheetmusicProvider(SheetmusicProvider):
    async def get_url(self, object_name: str) -> SheetmusicURLResponse:
        return SheetmusicURLResponse(
            url=f"https://mock.example.com/{object_name}",
            expires_at=datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=1),
        )
