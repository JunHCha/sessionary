from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.auth.access import authenticated_user
from app.containers.application import ApplicationContainer
from app.db.tables import User
from app.session.models import SessionDetailResponse
from app.session.service import SessionService
from app.ticket.service import TicketService

app_router = APIRouter()


@app_router.get(
    "/{session_id}",
    response_model=SessionDetailResponse,
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Access denied"},
        404: {"description": "Session not found"},
    },
)
@inject
async def get_session_detail(
    session_id: int,
    user: User = Depends(authenticated_user),
    session_service: SessionService = Depends(
        Provide[ApplicationContainer.services.session_service]
    ),
    ticket_service: TicketService = Depends(
        Provide[ApplicationContainer.services.ticket_service]
    ),
):
    session_detail = await session_service.get_session_detail(session_id)
    if not session_detail:
        raise HTTPException(status_code=404, detail="Session not found")

    user_with_subscription = await ticket_service.get_user_or_raise(user.id)

    can_access = await ticket_service.can_access_lesson(
        user_with_subscription, session_detail.lecture.id
    )
    if not can_access:
        raise HTTPException(status_code=403, detail="Access denied")

    return session_detail
