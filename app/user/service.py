import abc
from typing import List

from fastapi import Depends

from app.db.tables import User
from app.user.api.schemas import UserRead
from app.user.repository import BaseUserRepository, get_user_repository


class BaseUserService(abc.ABC):
    def __init__(self, repository: BaseUserRepository) -> None:
        self.user_repository = repository

    @abc.abstractmethod
    async def get_artists(self) -> List[User]:
        raise NotImplementedError


class UserService(BaseUserService):
    async def get_artists(self) -> list[UserRead]:
        results = await self.user_repository.get_artists()
        return results


def get_user_service(repository=Depends(get_user_repository)):
    return UserService(repository=repository)
