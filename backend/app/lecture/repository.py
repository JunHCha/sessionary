import abc

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app.db import tables as tb
from app.db.session import SessionManager
from app.lecture.models import LectureDetail, LectureInList, PaginationMeta
from app.lesson.models import LessonInLecture


class BaseLectureRepository(abc.ABC):
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    @abc.abstractmethod
    async def fetch_lectures(
        self, page: int, per_page: int
    ) -> tuple[list[LectureInList], PaginationMeta]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_lecture(self, lecture_id: int) -> LectureDetail:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_lecture(self, title: str, description: str) -> LectureDetail:
        raise NotImplementedError


class LectureRepository(BaseLectureRepository):
    async def fetch_lectures(
        self, page: int, per_page: int
    ) -> tuple[list[LectureInList], PaginationMeta]:
        async with self._session_manager.async_session() as session:
            total_items = (
                await session.execute(func.count(tb.Lecture.id))
            ).scalar_one()
            results = (
                (
                    await session.execute(
                        select(tb.Lecture)
                        .options(
                            joinedload(tb.Lecture.artist),
                            joinedload(tb.Lecture.lessons),
                        )
                        .offset((page - 1) * per_page)
                        .limit(per_page)
                        .order_by(tb.Lecture.time_updated.desc())
                    )
                )
                .unique()
                .scalars()
                .all()
            )
            return self._map_to_lecture_list(results, total_items, page, per_page)

    def _map_to_lecture_list(
        self, results, total_items: int, page: int, per_page: int
    ) -> tuple[list[LectureInList], PaginationMeta]:
        from app.lecture.models import ArtistInfoInLecture

        lecture_list = []
        for row in results:
            lessons = [
                LessonInLecture(
                    id=item.id,
                    title=item.title,
                    length_sec=item.length_sec,
                    lecture_ordering=item.lecture_ordering,
                    time_created=item.time_created,
                    time_updated=item.time_updated,
                )
                for item in row.lessons
            ]
            artist = None
            if row.artist:
                artist = ArtistInfoInLecture(
                    id=row.artist.id,
                    nickname=row.artist.nickname,
                    is_artist=row.artist.is_artist,
                )
            lecture_list.append(
                LectureInList(
                    id=row.id,
                    thumbnail=row.thumbnail,
                    title=row.title,
                    artist=artist,
                    lessons=lessons,
                    description=row.description,
                    tags=row.tags,
                    length_sec=row.length_sec,
                    lecture_count=row.lecture_count,
                    time_created=row.time_created,
                    time_updated=row.time_updated,
                )
            )
        return (
            lecture_list,
            PaginationMeta(
                total_items=total_items,
                total_pages=(total_items + per_page - 1) // per_page,
                curr_page=page,
                per_page=per_page,
            ),
        )

    async def get_lecture(self, lecture_id: int) -> LectureDetail:
        async with self._session_manager.async_session() as session:
            result = (
                (
                    await session.execute(
                        select(tb.Lecture)
                        .options(
                            joinedload(tb.Lecture.artist),
                            joinedload(tb.Lecture.lessons),
                        )
                        .filter(tb.Lecture.id == lecture_id)
                    )
                )
                .unique()
                .scalar_one()
            )
            return self._map_to_lecture_detail(result)

    def _map_to_lecture_detail(self, result) -> LectureDetail:
        lessons = [
            LessonInLecture(
                id=item.id,
                title=item.title,
                length_sec=item.length_sec,
                lecture_ordering=item.lecture_ordering,
                time_created=item.time_created,
                time_updated=item.time_updated,
            )
            for item in result.lessons
        ]
        artist = None
        if result.artist:
            from app.lecture.models import ArtistInfoInLecture

            artist = ArtistInfoInLecture(
                id=result.artist.id,
                nickname=result.artist.nickname,
                is_artist=result.artist.is_artist,
            )
        return LectureDetail(
            id=result.id,
            title=result.title,
            lessons=lessons,
            artist=artist,
            description=result.description,
            thumbnail=result.thumbnail,
            tags=result.tags,
            length_sec=result.length_sec,
            lecture_count=result.lecture_count,
            time_created=result.time_created,
            time_updated=result.time_updated,
        )

    async def create_lecture(self, title: str, description: str) -> LectureDetail:
        async with self._session_manager.async_session() as session:
            new_lecture = tb.Lecture(title=title, description=description)
            session.add(new_lecture)
            await session.flush()
            await session.commit()
            return LectureDetail(
                id=new_lecture.id,
                title=new_lecture.title,
                artist=None,
                lessons=[],
                description=new_lecture.description,
                thumbnail=new_lecture.thumbnail,
                tags=new_lecture.tags,
                length_sec=new_lecture.length_sec,
                lecture_count=new_lecture.lecture_count,
                time_created=new_lecture.time_created,
                time_updated=new_lecture.time_updated,
            )
