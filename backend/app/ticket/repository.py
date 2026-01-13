import abc
import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import tables as tb
from app.db.session import SessionManager


class BaseTicketRepository(abc.ABC):
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    @abc.abstractmethod
    async def get_ticket_usage(
        self, user_id: uuid.UUID, lecture_id: int
    ) -> tb.TicketUsage | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_ticket_usage(
        self, user_id: uuid.UUID, lecture_id: int
    ) -> tb.TicketUsage:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_user(self, user_id: uuid.UUID) -> tb.User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def decrease_user_ticket_count(self, user_id: uuid.UUID) -> tb.User:
        raise NotImplementedError


class TicketRepository(BaseTicketRepository):
    async def get_ticket_usage(
        self, user_id: uuid.UUID, lecture_id: int
    ) -> tb.TicketUsage | None:
        async with self._session_manager.async_session() as session:
            result = await session.execute(
                select(tb.TicketUsage).where(
                    tb.TicketUsage.user_id == user_id,
                    tb.TicketUsage.lecture_id == lecture_id,
                    tb.TicketUsage.used_at
                    > datetime.datetime.now(datetime.timezone.utc)
                    - datetime.timedelta(weeks=1),
                )
            )
            return result.scalar_one_or_none()

    async def create_ticket_usage(
        self, user_id: uuid.UUID, lecture_id: int
    ) -> tb.TicketUsage:
        async with self._session_manager.async_session() as session:
            ticket_usage = tb.TicketUsage(
                user_id=user_id,
                lecture_id=lecture_id,
            )
            session.add(ticket_usage)
            await session.flush()
            await session.refresh(ticket_usage)
            return ticket_usage

    async def get_user(self, user_id: uuid.UUID) -> tb.User | None:
        async with self._session_manager.async_session() as session:
            result = await session.execute(
                select(tb.User)
                .options(selectinload(tb.User.subscription))
                .where(tb.User.id == user_id)
            )
            return result.scalar_one_or_none()

    async def decrease_user_ticket_count(self, user_id: uuid.UUID) -> tb.User:
        async with self._session_manager.async_session() as session:
            result = await session.execute(select(tb.User).where(tb.User.id == user_id))
            user = result.scalar_one()
            user.ticket_count -= 1
            await session.flush()
            await session.refresh(user)
            await session.commit()
            return user
