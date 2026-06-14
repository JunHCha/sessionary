from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.auth.access import authenticated_user, superuser
from app.containers.application import ApplicationContainer
from app.db.tables import User
from app.lesson.models import (
    CreateLessonBody,
    LessonAdminSchema,
    UpdateLessonBody,
)
from app.lesson.repository import BaseLessonRepository
from app.lesson.service import LessonService
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

    user_with_subscription = await ticket_service.get_user_or_raise(user.id)
    if not user_with_subscription:
        raise HTTPException(status_code=404, detail="User not found")

    can_access = await ticket_service.can_access_lesson(
        user_with_subscription, lesson.lecture_id
    )
    if not can_access:
        raise HTTPException(status_code=403, detail="Access denied")

    if not lesson.video_url:
        raise HTTPException(status_code=404, detail="Video not available for this lesson")

    return await video_provider.get_video_url(lesson.video_url)


@app_router.post("", response_model=LessonAdminSchema, status_code=201)
@inject
async def create_lesson(
    body: CreateLessonBody,
    user: User = Depends(superuser),
    lesson_service: LessonService = Depends(
        Provide[ApplicationContainer.services.lesson_service]
    ),
):
    fields = body.model_dump()
    fields["artist_id"] = user.id
    fields["subtitles"] = list(fields.get("subtitles", []))
    fields["playing_guide"] = list(fields.get("playing_guide", []))
    fields.setdefault("sheetmusic_url", "")
    fields.setdefault("video_url", "")
    lesson = await lesson_service.create_lesson(fields)
    return LessonAdminSchema(data=lesson)


@app_router.patch("/{lesson_id}", response_model=LessonAdminSchema)
@inject
async def update_lesson(
    lesson_id: int,
    body: UpdateLessonBody,
    user: User = Depends(superuser),
    lesson_service: LessonService = Depends(
        Provide[ApplicationContainer.services.lesson_service]
    ),
):
    fields = body.model_dump(exclude_unset=True)
    lesson = await lesson_service.update_lesson(lesson_id, fields)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return LessonAdminSchema(data=lesson)
