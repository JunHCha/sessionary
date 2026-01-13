from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.auth.access import authenticated_user
from app.containers.application import ApplicationContainer
from app.db.tables import User
from app.lesson.repository import BaseLessonRepository
from app.ticket.service import TicketService
from app.video.models import VideoURLResponse
from app.video.service import VideoProvider

app_router = APIRouter()


@app_router.get("/{lesson_id}/video", response_model=VideoURLResponse)
@inject
async def get_lesson_video(
    lesson_id: int,
    user: User = Depends(authenticated_user),
    lesson_repository: BaseLessonRepository = Depends(
        Provide[ApplicationContainer.services.lesson_repository]
    ),
    ticket_service: TicketService = Depends(
        Provide[ApplicationContainer.services.ticket_service]
    ),
    video_provider: VideoProvider = Depends(
        Provide[ApplicationContainer.services.video_provider]
    ),
):
    lesson = await lesson_repository.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if not lesson.lecture_id:
        raise HTTPException(status_code=400, detail="Lesson has no lecture")

    user_with_subscription = await ticket_service.repository.get_user(user.id)
    if not user_with_subscription:
        raise HTTPException(status_code=404, detail="User not found")

    can_access = await ticket_service.can_access_lesson(
        user_with_subscription, lesson.lecture_id
    )
    if not can_access:
        raise HTTPException(status_code=403, detail="Access denied")

    return await video_provider.get_video_url(lesson.video_url)
