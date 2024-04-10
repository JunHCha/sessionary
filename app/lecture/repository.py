import abc

from fastapi import Depends

from app.db.dependency import get_session


class BaseLectureRepository(abc.ABC): ...


class LectureRepository(BaseLectureRepository): ...


def get_lecture_repository(session=Depends(get_session)) -> BaseLectureRepository:
    return LectureRepository(session=session)
