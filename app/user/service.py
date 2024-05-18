import abc
from typing import List

from app.models import UserArtistInfo
from app.user.repository import BaseUserRepository


class BaseUserService(abc.ABC):
    def __init__(self, repository: BaseUserRepository) -> None:
        self.user_repository = repository

    @abc.abstractmethod
    async def get_artists(self) -> List[UserArtistInfo]:
        raise NotImplementedError


class UserService(BaseUserService):
    async def get_artists(self) -> list[UserArtistInfo]:
        results = await self.user_repository.get_artists()
        return results
