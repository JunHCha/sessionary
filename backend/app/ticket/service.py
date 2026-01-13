import datetime
import uuid

from fastapi import HTTPException

from app.db import tables as tb
from app.ticket.models import LectureAccessStatus
from app.ticket.repository import BaseTicketRepository


class TicketService:
    TICKET_VALIDITY_WEEKS = 1

    def __init__(self, repository: BaseTicketRepository) -> None:
        self.repository = repository

    def _is_unlimited_subscription(self, user: tb.User) -> bool:
        if not user.subscription:
            return False

        subscription_name = user.subscription.name.lower()
        if subscription_name not in ["personal", "group", "experimental"]:
            return False

        if not user.subscription.is_active:
            return False

        if user.expires_at:
            now = datetime.datetime.now(datetime.timezone.utc)
            if user.expires_at.tzinfo is None:
                now = now.replace(tzinfo=None)
            if user.expires_at < now:
                return False

        return True

    async def get_lecture_access_status(
        self, user: tb.User, lecture_id: int
    ) -> LectureAccessStatus:
        if self._is_unlimited_subscription(user):
            return LectureAccessStatus(
                accessible=True,
                reason="unlimited",
                expires_at=None,
                ticket_count=user.ticket_count,
            )

        ticket_usage = await self.repository.get_ticket_usage(user.id, lecture_id)

        if ticket_usage:
            expires_at = ticket_usage.used_at + datetime.timedelta(
                weeks=self.TICKET_VALIDITY_WEEKS
            )
            return LectureAccessStatus(
                accessible=True,
                reason="ticket_used",
                expires_at=expires_at,
                ticket_count=user.ticket_count,
            )

        if user.ticket_count <= 0:
            return LectureAccessStatus(
                accessible=False,
                reason="no_ticket",
                expires_at=None,
                ticket_count=0,
            )

        return LectureAccessStatus(
            accessible=False,
            reason=None,
            expires_at=None,
            ticket_count=user.ticket_count,
        )

    async def use_ticket(self, user: tb.User, lecture_id: int) -> LectureAccessStatus:
        if user.ticket_count <= 0:
            raise HTTPException(status_code=403, detail="No tickets available")

        existing_usage = await self.repository.get_ticket_usage(user.id, lecture_id)
        if existing_usage:
            expires_at = existing_usage.used_at + datetime.timedelta(
                weeks=self.TICKET_VALIDITY_WEEKS
            )
            return LectureAccessStatus(
                accessible=True,
                reason="ticket_used",
                expires_at=expires_at,
                ticket_count=user.ticket_count,
            )

        ticket_usage = await self.repository.create_ticket_usage(user.id, lecture_id)
        updated_user = await self.repository.decrease_user_ticket_count(user.id)

        expires_at = ticket_usage.used_at + datetime.timedelta(
            weeks=self.TICKET_VALIDITY_WEEKS
        )
        return LectureAccessStatus(
            accessible=True,
            reason="ticket_used",
            expires_at=expires_at,
            ticket_count=updated_user.ticket_count,
        )

    async def can_access_lesson(self, user: tb.User, lecture_id: int) -> bool:
        if self._is_unlimited_subscription(user):
            return True

        ticket_usage = await self.repository.get_ticket_usage(user.id, lecture_id)
        return ticket_usage is not None
