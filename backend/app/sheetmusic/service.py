import abc

from app.sheetmusic.models import SheetmusicURLResponse


class SheetmusicProvider(abc.ABC):
    @abc.abstractmethod
    async def get_url(self, object_name: str) -> SheetmusicURLResponse:
        raise NotImplementedError

    @abc.abstractmethod
    async def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        """업로드 후 저장 object key 반환"""
        raise NotImplementedError
