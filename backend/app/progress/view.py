from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound

from app.auth.access import authenticated_user
from app.containers.application import ApplicationContainer
from app.db.tables import User
from app.lecture.service import BaseLectureService
from app.progress.models import LectureProgressData, PositionReport
from app.progress.service import ProgressService

app_router = APIRouter()


@app_router.post(
    "/lesson/{lesson_id}",
    response_model=LectureProgressData,
    responses={
        401: {"description": "Missing token or inactive user."},
        404: {"description": "Lesson not found."},
    },
)
@inject
async def mark_lesson_complete(
    lesson_id: int,
    user: User = Depends(authenticated_user),
    progress_service: ProgressService = Depends(
        Provide[ApplicationContainer.services.progress_service]
    ),
    lecture_service: BaseLectureService = Depends(
        Provide[ApplicationContainer.services.lecture_service]
    ),
):
    try:
        progress = await progress_service.mark_complete(user.id, lesson_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Lesson not found")
    lecture = await lecture_service.get_lecture_detail(progress.lecture_id)
    return await progress_service.get_lecture_progress(user.id, lecture)


@app_router.put(
    "/lesson/{lesson_id}/position",
    response_model=LectureProgressData,
    responses={
        401: {"description": "Missing token or inactive user."},
        404: {"description": "Lesson not found."},
    },
)
@inject
async def report_lesson_position(
    lesson_id: int,
    report: PositionReport,
    user: User = Depends(authenticated_user),
    progress_service: ProgressService = Depends(
        Provide[ApplicationContainer.services.progress_service]
    ),
):
    try:
        return await progress_service.report_position(
            user.id, lesson_id, report.position_sec, report.duration_sec
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Lesson not found")
