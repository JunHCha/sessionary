from fastapi import Depends

from app.depends.db import get_session
from app.lecture.repository import BaseLectureRepository, LectureRepository
from app.user.repository import BaseUserRepository, UserRepository


def get_user_repository(session=Depends(get_session)) -> BaseUserRepository:
    return UserRepository(session=session)


def get_lecture_repository(session=Depends(get_session)) -> BaseLectureRepository:
    return LectureRepository(session=session)
