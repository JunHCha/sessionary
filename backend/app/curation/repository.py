from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from app.db import tables as tb
from app.db.session import SessionManager
from app.db.tables import CurationSection


class CurationRepository:
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    async def set_section(
        self, section: CurationSection, lecture_ids: list[int]
    ) -> None:
        async with self._session_manager.async_session() as session:
            await session.execute(
                delete(tb.HomeCuration).where(tb.HomeCuration.section == section)
            )
            for ordering, lecture_id in enumerate(lecture_ids):
                session.add(
                    tb.HomeCuration(
                        section=section, lecture_id=lecture_id, ordering=ordering
                    )
                )
            await session.commit()

    async def get_section_lectures(
        self, section: CurationSection
    ) -> list[tb.Lecture]:
        async with self._session_manager.async_session() as session:
            rows = (
                (
                    await session.execute(
                        select(tb.HomeCuration)
                        .options(
                            joinedload(tb.HomeCuration.lecture).joinedload(
                                tb.Lecture.artist
                            ),
                            joinedload(tb.HomeCuration.lecture).joinedload(
                                tb.Lecture.lessons
                            ),
                        )
                        .where(tb.HomeCuration.section == section)
                        .order_by(tb.HomeCuration.ordering)
                    )
                )
                .unique()
                .scalars()
                .all()
            )
            return [row.lecture for row in rows]
