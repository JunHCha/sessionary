from app.curation.models import CurationData
from app.curation.repository import CurationRepository
from app.db import tables as tb
from app.db.tables import CurationSection
from app.lecture.models import ArtistInfoInLecture, LectureInList
from app.lesson.models import LessonInLecture


class CurationService:
    def __init__(self, repository: CurationRepository) -> None:
        self.repository = repository

    async def set_section(
        self, section: CurationSection, lecture_ids: list[int]
    ) -> None:
        await self.repository.set_section(section, lecture_ids)

    async def get_curation(self) -> CurationData:
        trending = await self.repository.get_section_lectures(CurationSection.TRENDING)
        new = await self.repository.get_section_lectures(CurationSection.NEW)
        return CurationData(
            TRENDING=[self._to_list_item(x) for x in trending],
            NEW=[self._to_list_item(x) for x in new],
        )

    def _to_list_item(self, lecture: tb.Lecture) -> LectureInList:
        artist = None
        if lecture.artist:
            artist = ArtistInfoInLecture(
                id=lecture.artist.id,
                nickname=lecture.artist.nickname,
                is_artist=lecture.artist.is_artist,
            )
        lessons = [
            LessonInLecture(
                id=lesson.id,
                title=lesson.title,
                length_sec=lesson.length_sec,
                lecture_ordering=lesson.lecture_ordering,
                time_created=lesson.time_created,
                time_updated=lesson.time_updated,
            )
            for lesson in lecture.lessons
        ]
        return LectureInList(
            id=lecture.id,
            thumbnail=lecture.thumbnail,
            title=lecture.title,
            artist=artist,
            lessons=lessons,
            description=lecture.description,
            tags=lecture.tags,
            length_sec=lecture.length_sec,
            lecture_count=lecture.lecture_count,
            time_created=lecture.time_created,
            time_updated=lecture.time_updated,
        )
