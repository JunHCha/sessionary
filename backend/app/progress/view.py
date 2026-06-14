from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.auth.access import authenticated_user
from app.containers.application import ApplicationContainer
from app.db.tables import User
from app.lecture.service import BaseLectureService
from app.progress.models import LectureProgressData
from app.progress.service import ProgressService

app_router = APIRouter()


@app_router.post(
    "/lesson/{lesson_id}",
    response_model=LectureProgressData,
    responses={401: {"description": "Missing token or inactive user."}},
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
    progress = await progress_service.mark_complete(user.id, lesson_id)
    lecture = await lecture_service.get_lecture_detail(progress.lecture_id)
    return await progress_service.get_lecture_progress(user.id, lecture)
