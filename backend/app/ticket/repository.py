import abc
import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy import select, update
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

    @abc.abstractmethod
    async def use_ticket_atomically(
        self, user_id: uuid.UUID, lecture_id: int, expected_ticket_count: int
    ) -> tuple[tb.TicketUsage, tb.User]:
        raise NotImplementedError


class TicketRepository(BaseTicketRepository):
    async def get_ticket_usage(
        self, user_id: uuid.UUID, lecture_id: int
    ) -> tb.TicketUsage | None:
        async with self._session_manager.async_session() as session:
            now = datetime.datetime.now(datetime.timezone.utc)
            one_week_ago = now - datetime.timedelta(weeks=1)
            result = await session.execute(
                select(tb.TicketUsage).where(
                    tb.TicketUsage.user_id == user_id,
                    tb.TicketUsage.lecture_id == lecture_id,
                    tb.TicketUsage.used_at > one_week_ago,
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
            await session.commit()
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
            stmt = (
                update(tb.User)
                .where(
                    tb.User.id == user_id,
                    tb.User.ticket_count > 0,
                )
                .values(ticket_count=tb.User.ticket_count - 1)
                .returning(tb.User)
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user is None:
                raise HTTPException(
                    status_code=403, detail="No tickets available or user not found"
                )

            await session.commit()
            await session.refresh(user, ["subscription"])
            return user

    async def use_ticket_atomically(
        self, user_id: uuid.UUID, lecture_id: int, expected_ticket_count: int
    ) -> tuple[tb.TicketUsage, tb.User]:
        async with self._session_manager.async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(tb.User).where(
                        tb.User.id == user_id,
                        tb.User.ticket_count == expected_ticket_count,
                    )
                )
                user = result.scalar_one_or_none()
                if not user:
                    raise ValueError(
                        "User not found or ticket count changed (concurrent modification)"
                    )

                ticket_usage = tb.TicketUsage(
                    user_id=user_id,
                    lecture_id=lecture_id,
                )
                session.add(ticket_usage)
                await session.flush()
                await session.refresh(ticket_usage)

                user.ticket_count -= 1
                await session.flush()
                await session.refresh(user)

                return ticket_usage, user
