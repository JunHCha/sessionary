from fastapi import Depends

from app.depends.repository import get_lecture_repository, get_user_repository
from app.lecture.repository import BaseLectureRepository
from app.lecture.service import BaseLectureService, LectureService
from app.user.service import UserService


def get_user_service(repository=Depends(get_user_repository)):
    return UserService(repository=repository)


def get_lecture_service(
    repository: BaseLectureRepository = Depends(get_lecture_repository),
) -> BaseLectureService:
    return LectureService(repository)
