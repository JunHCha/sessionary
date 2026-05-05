import abc

from app.sheetmusic.models import SheetmusicURLResponse


class SheetmusicProvider(abc.ABC):
    @abc.abstractmethod
    async def get_url(self, object_name: str) -> SheetmusicURLResponse:
        raise NotImplementedError
