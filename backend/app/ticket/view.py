from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.auth.access import authenticated_user
from app.containers.application import ApplicationContainer
from app.db.tables import User
from app.ticket.models import LectureAccessStatus
from app.ticket.service import TicketService

app_router = APIRouter()


@app_router.get("/lecture/{lecture_id}", response_model=LectureAccessStatus)
@inject
async def get_lecture_access_status(
    lecture_id: int,
    user: User = Depends(authenticated_user),
    ticket_service: TicketService = Depends(
        Provide[ApplicationContainer.services.ticket_service]
    ),
):
    user_with_subscription = await ticket_service.repository.get_user(user.id)
    if not user_with_subscription:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="User not found")
    return await ticket_service.get_lecture_access_status(
        user_with_subscription, lecture_id
    )


@app_router.post("/lecture/{lecture_id}", response_model=LectureAccessStatus)
@inject
async def use_ticket(
    lecture_id: int,
    user: User = Depends(authenticated_user),
    ticket_service: TicketService = Depends(
        Provide[ApplicationContainer.services.ticket_service]
    ),
):
    user_with_subscription = await ticket_service.repository.get_user(user.id)
    if not user_with_subscription:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="User not found")
    return await ticket_service.use_ticket(user_with_subscription, lecture_id)
