# Sessionary Admin Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `/admin` 서브라우트에 관리자(`is_superuser`) 전용 페이지(렉처 생성/편집, 레슨 생성/업로드, 홈 큐레이션 선정)를 구현하고, 미인증·비관리자는 `/home`으로 리다이렉트한다.

**Architecture:** 백엔드는 기존 도메인 모듈(lecture/lesson)에 `superuser`-gated 쓰기 엔드포인트를 추가하고, 홈 큐레이션은 신규 `curation` 모듈 + `home_curation` 테이블로 분리한다. 업로드는 백엔드 멀티파트 → Provider(MinIO dev / mock test)로 저장. 프론트는 CSR 전용 `/admin` 라우트 그룹 + auth store 확장으로 가드한다. OpenAPI 계약은 스냅샷 기반이라 백엔드 변경 후 `make gen-client`로 재생성·커밋한다.

**Tech Stack:** FastAPI / SQLAlchemy(async) / dependency-injector / Alembic / pytest(SQLite). SvelteKit + Svelte 5 Runes / flowbite-svelte / Vitest / Playwright. OpenAPI codegen(`@hey-api/openapi-ts`).

---

## 핵심 계약 / 참조 (구현 전 숙지)

- admin = `User.is_superuser`. 디펜던시 `app/auth/access.py::superuser` 재사용.
- "레슨"=DB `Lesson`(`backend/app/db/tables.py:204`). 컬럼: `lecture_id`, `title`, `length_sec`, `sheetmusic_url`, `video_url`, `text`, `lecture_ordering`, `session_type`(Enum), `subtitles`(JSON), `playing_guide`(JSON), `sync_offset`, `artist_id`(NOT NULL).
- `Subtitle` 스키마: `{ timestamp_ms: int>=0, text: str }` (`app/session/models.py:27`).
- `PlayingGuideStep`: `{ step, title, description, start_time, end_time, tip? }` (`app/session/models.py:32`).
- DI 등록 지점: `backend/app/containers/services.py`. 라우터 등록 + wiring: `backend/app/main.py` (`create_container().wire(modules=[...])` + `api_router.include_router(...)`).
- **테스트 wiring**: `backend/tests/conftest.py:test_container`의 `container.wire(modules=[...])` 리스트에도 신규 view 모듈을 추가해야 한다.
- 테스트 픽스처(`backend/tests/api/conftest.py`): `client`(비인증), `authorized_client`(일반), `authorized_client_artist`(아티스트, 비superuser), `authorized_client_admin`(superuser). 테스트 provider는 `mock`.
- 프론트 API: `import { fnNameOperationId } from '$lib/api'`. 생성 클라이언트는 operationId 기반 함수명. 변경 후 함수명은 `frontend/src/lib/api/client/services.gen.ts`에서 확인.
- 프론트 포맷: 탭(width 4), 싱글쿼트, 세미콜론 없음, trailing comma 없음, print width 100. Svelte 5 Runes만(`$:` 금지). `data-testid` 부착.
- 작업 브랜치: 이미 `cc/sharp-bassi-b4ef61`(비-main). 각 태스크 후 커밋.

---

## Phase 1 — 백엔드: Lecture 편집

### Task 1: Lecture PATCH 스키마 + 서비스/레포 + 엔드포인트

**Files:**
- Modify: `backend/app/lecture/models.py` (스키마 추가)
- Modify: `backend/app/lecture/service.py` (update 메서드)
- Modify: `backend/app/lecture/repository.py` (update 메서드)
- Modify: `backend/app/lecture/view.py` (PATCH 라우트)
- Test: `backend/tests/api/test_lecture_admin.py` (신규)

- [ ] **Step 1: 실패하는 테스트 작성** — `backend/tests/api/test_lecture_admin.py`

```python
import datetime
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def one_lecture(test_session: AsyncSession) -> None:
    now = datetime.datetime.now()
    async with test_session.begin():
        test_session.add(
            Lecture(
                id=1,
                artist_id=None,
                thumbnail=None,
                title="old title",
                description="old desc",
                tags=("원곡카피", "Easy"),
                length_sec=0,
                time_created=now,
                time_updated=now,
            )
        )
    await test_session.commit()


async def test_patch_lecture_updates_fields(
    authorized_client_admin: AsyncClient, one_lecture
):
    body = {
        "title": "new title",
        "description": "new desc",
        "tags": ["해석버전", "Advanced"],
    }
    response = await authorized_client_admin.patch("/lecture/1", json=body)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == "new title"
    assert data["description"] == "new desc"
    assert data["tags"] == ["해석버전", "Advanced"]


async def test_patch_lecture_partial_keeps_other_fields(
    authorized_client_admin: AsyncClient, one_lecture
):
    response = await authorized_client_admin.patch(
        "/lecture/1", json={"title": "only title"}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == "only title"
    assert data["description"] == "old desc"


async def test_patch_lecture_forbidden_for_non_superuser(
    authorized_client_artist: AsyncClient, one_lecture
):
    response = await authorized_client_artist.patch(
        "/lecture/1", json={"title": "x"}
    )
    assert response.status_code == 403
```

- [ ] **Step 2: 실패 확인** — Run: `cd backend && uv run pytest tests/api/test_lecture_admin.py -v`  Expected: FAIL (404/405 또는 라우트 없음).

- [ ] **Step 3: 스키마 추가** — `backend/app/lecture/models.py` 끝에 추가

```python
class UpdateLectureBody(BaseSchema):
    title: str | None = None
    description: str | None = None
    tags: tuple[LectureType, DifficultyLevel] | None = None
    thumbnail: str | None = None
```

- [ ] **Step 4: 레포 update 추가** — `backend/app/lecture/repository.py`의 `BaseLectureRepository`에 추상 메서드 + `LectureRepository`에 구현

```python
    # BaseLectureRepository 내부
    @abc.abstractmethod
    async def update_lecture(self, lecture_id: int, fields: dict) -> LectureDetail:
        raise NotImplementedError
```

```python
    # LectureRepository 내부
    async def update_lecture(self, lecture_id: int, fields: dict) -> LectureDetail:
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
            for key, value in fields.items():
                setattr(result, key, value)
            await session.commit()
            await session.refresh(result)
            return self._map_to_lecture_detail(result)
```

- [ ] **Step 5: 서비스 update 추가** — `backend/app/lecture/service.py` (Base에 abstractmethod, LectureService에 구현)

```python
    # BaseLectureService
    @abc.abstractmethod
    async def update_lecture(self, lecture_id: int, fields: dict) -> LectureDetail:
        raise NotImplementedError
```

```python
    # LectureService
    async def update_lecture(self, lecture_id: int, fields: dict) -> LectureDetail:
        return await self.lecture_repository.update_lecture(lecture_id, fields)
```

- [ ] **Step 6: PATCH 라우트 추가** — `backend/app/lecture/view.py`

```python
from app.lecture.models import (
    CreateLectureBody,
    CreateLectureResponseSchema,
    FetchRecommendedLecuturesSchema,
    GetLectureSchema,
    UpdateLectureBody,
)


@app_router.patch("/{lecture_id}", response_model=GetLectureSchema)
@inject
async def update_lecture(
    lecture_id: int,
    body: UpdateLectureBody,
    lecture_svc: BaseLectureService = Depends(
        Provide[ApplicationContainer.services.lecture_service]
    ),
    user=Depends(superuser),
):
    fields = body.model_dump(exclude_unset=True)
    lecture = await lecture_svc.update_lecture(lecture_id, fields)
    return GetLectureSchema(data=lecture)
```

- [ ] **Step 7: 통과 확인** — Run: `cd backend && uv run pytest tests/api/test_lecture_admin.py -v`  Expected: PASS (3 passed).

- [ ] **Step 8: 커밋**

```bash
git add backend/app/lecture backend/tests/api/test_lecture_admin.py
git commit -m "✨ PATCH /lecture/{id} 렉처 속성 편집 엔드포인트"
```

---

## Phase 2 — 백엔드: Provider 업로드 + Lesson 쓰기

### Task 2: Provider에 upload 메서드 추가 (mock/minio/cloudflare)

**Files:**
- Modify: `backend/app/video/service.py`, `backend/app/video/mock.py`, `backend/app/video/minio.py`, `backend/app/video/cloudflare.py`
- Modify: `backend/app/sheetmusic/service.py`, `backend/app/sheetmusic/mock.py`, `backend/app/sheetmusic/minio.py`
- Test: `backend/tests/test_provider_upload.py` (신규)

- [ ] **Step 1: 실패 테스트** — `backend/tests/test_provider_upload.py`

```python
import pytest

from app.video.mock import MockVideoProvider
from app.sheetmusic.mock import MockSheetmusicProvider

pytest_plugins = ["tests.conftest"]


async def test_mock_video_upload_returns_object_key():
    provider = MockVideoProvider()
    key = await provider.upload("clip.mp4", b"data", "video/mp4")
    assert key == "clip.mp4"


async def test_mock_sheetmusic_upload_returns_object_key():
    provider = MockSheetmusicProvider()
    key = await provider.upload("tab.musicxml", b"<xml/>", "application/xml")
    assert key == "tab.musicxml"
```

- [ ] **Step 2: 실패 확인** — Run: `cd backend && uv run pytest tests/test_provider_upload.py -v`  Expected: FAIL (`upload` 미정의).

- [ ] **Step 3: 추상 메서드 추가** — `backend/app/video/service.py`의 `VideoProvider`에:

```python
    @abc.abstractmethod
    async def upload(
        self, object_name: str, data: bytes, content_type: str
    ) -> str:
        """업로드 후 저장 object key 반환"""
        raise NotImplementedError
```

`backend/app/sheetmusic/service.py`의 `SheetmusicProvider`에 동일 시그니처 추가.

- [ ] **Step 4: 구현 추가**

`backend/app/video/mock.py` `MockVideoProvider`에:

```python
    async def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        return object_name
```

`backend/app/sheetmusic/mock.py` `MockSheetmusicProvider`에 동일.

`backend/app/video/minio.py` `MinIOVideoProvider`에 (io import 추가):

```python
    async def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        import io

        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=io.BytesIO(data),
            length=len(data),
            content_type=content_type,
        )
        return object_name
```

`backend/app/sheetmusic/minio.py` `MinIOSheetmusicProvider`에 동일 패턴(`self.bucket_name` 사용).

`backend/app/video/cloudflare.py` `CloudflareVideoProvider`에 스텁:

```python
    async def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        raise NotImplementedError("Cloudflare 업로드는 이번 범위 밖입니다")
```

- [ ] **Step 5: 통과 확인** — Run: `cd backend && uv run pytest tests/test_provider_upload.py -v`  Expected: PASS.

- [ ] **Step 6: 커밋**

```bash
git add backend/app/video backend/app/sheetmusic backend/tests/test_provider_upload.py
git commit -m "✨ Video/Sheetmusic Provider upload 메서드 추가"
```

### Task 3: LessonService + 레포 쓰기 + POST/PATCH /lesson

**Files:**
- Create: `backend/app/lesson/service.py`
- Modify: `backend/app/lesson/models.py` (Pydantic 스키마)
- Modify: `backend/app/lesson/repository.py` (create/update)
- Modify: `backend/app/lesson/view.py` (POST, PATCH 라우트)
- Modify: `backend/app/containers/services.py` (lesson_service 등록)
- Modify: `backend/app/main.py`, `backend/tests/conftest.py` (이미 lesson.view wired — 변경 불필요)
- Test: `backend/tests/api/test_lesson_admin.py` (신규)

- [ ] **Step 1: 실패 테스트** — `backend/tests/api/test_lesson_admin.py`

```python
import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def one_lecture(test_session: AsyncSession) -> None:
    now = datetime.datetime.now()
    async with test_session.begin():
        test_session.add(
            Lecture(
                id=1, artist_id=None, thumbnail=None, title="L", description="d",
                tags=None, length_sec=0, time_created=now, time_updated=now,
            )
        )
    await test_session.commit()


async def test_create_lesson(authorized_client_admin: AsyncClient, one_lecture):
    body = {
        "lecture_id": 1,
        "title": "lesson A",
        "session_type": "PLAY",
        "lecture_ordering": 0,
        "length_sec": 120,
        "text": "intro",
    }
    response = await authorized_client_admin.post("/lesson", json=body)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["id"] > 0
    assert data["title"] == "lesson A"


async def test_create_lesson_forbidden_for_artist(
    authorized_client_artist: AsyncClient, one_lecture
):
    response = await authorized_client_artist.post(
        "/lesson", json={"lecture_id": 1, "title": "x", "length_sec": 0}
    )
    assert response.status_code == 403


async def test_patch_lesson_subtitles(
    authorized_client_admin: AsyncClient, one_lecture
):
    created = await authorized_client_admin.post(
        "/lesson",
        json={"lecture_id": 1, "title": "L", "length_sec": 0},
    )
    lesson_id = created.json()["data"]["id"]
    subtitles = [{"timestamp_ms": 0, "text": "hi"}, {"timestamp_ms": 1000, "text": "yo"}]
    response = await authorized_client_admin.patch(
        f"/lesson/{lesson_id}", json={"subtitles": subtitles}
    )
    assert response.status_code == 200
    assert response.json()["data"]["subtitles"] == subtitles
```

- [ ] **Step 2: 실패 확인** — Run: `cd backend && uv run pytest tests/api/test_lesson_admin.py -v`  Expected: FAIL.

- [ ] **Step 3: 스키마** — `backend/app/lesson/models.py`에 추가

```python
from app.core.models import BaseModel, BaseSchema
from app.session.models import PlayingGuideStep, SessionType, Subtitle


class LessonAdminDetail(BaseModel):
    id: int
    lecture_id: int
    title: str
    length_sec: int
    text: str | None
    lecture_ordering: int
    session_type: SessionType | None
    sheetmusic_url: str | None
    video_url: str | None
    sync_offset: int
    subtitles: list[Subtitle]
    playing_guide: list[PlayingGuideStep]


class LessonAdminSchema(BaseSchema):
    data: LessonAdminDetail


class CreateLessonBody(BaseSchema):
    lecture_id: int
    title: str
    length_sec: int = 0
    text: str = ""
    lecture_ordering: int = 0
    session_type: SessionType | None = None
    sync_offset: int = 0
    subtitles: list[Subtitle] = []
    playing_guide: list[PlayingGuideStep] = []


class UpdateLessonBody(BaseSchema):
    title: str | None = None
    length_sec: int | None = None
    text: str | None = None
    lecture_ordering: int | None = None
    session_type: SessionType | None = None
    sync_offset: int | None = None
    subtitles: list[Subtitle] | None = None
    playing_guide: list[PlayingGuideStep] | None = None
```

> 참고: `Lesson.artist_id`는 NOT NULL. 생성 시 현재 superuser(`user.id`)를 `artist_id`로 채운다.

- [ ] **Step 4: 레포 create/update** — `backend/app/lesson/repository.py`

`BaseLessonRepository`에 추가:

```python
    @abc.abstractmethod
    async def create_lesson(self, fields: dict) -> tb.Lesson:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_lesson(self, lesson_id: int, fields: dict) -> tb.Lesson | None:
        raise NotImplementedError
```

`LessonRepository`에 구현 (JSON 직렬화를 위해 subtitles/playing_guide는 dict 리스트로 저장):

```python
    async def create_lesson(self, fields: dict) -> tb.Lesson:
        async with self._session_manager.async_session() as session:
            lesson = tb.Lesson(**fields)
            session.add(lesson)
            await session.commit()
            await session.refresh(lesson)
            return lesson

    async def update_lesson(self, lesson_id: int, fields: dict) -> tb.Lesson | None:
        async with self._session_manager.async_session() as session:
            result = await session.execute(
                select(tb.Lesson).where(tb.Lesson.id == lesson_id)
            )
            lesson = result.scalar_one_or_none()
            if lesson is None:
                return None
            for key, value in fields.items():
                setattr(lesson, key, value)
            await session.commit()
            await session.refresh(lesson)
            return lesson
```

- [ ] **Step 5: LessonService** — `backend/app/lesson/service.py` (신규)

```python
from app.lesson.models import LessonAdminDetail
from app.lesson.repository import BaseLessonRepository
from app.sheetmusic.service import SheetmusicProvider
from app.video.service import VideoProvider


class LessonService:
    def __init__(
        self,
        repository: BaseLessonRepository,
        video_provider: VideoProvider,
        sheetmusic_provider: SheetmusicProvider,
    ) -> None:
        self.repository = repository
        self.video_provider = video_provider
        self.sheetmusic_provider = sheetmusic_provider

    async def create_lesson(self, fields: dict) -> LessonAdminDetail:
        lesson = await self.repository.create_lesson(fields)
        return self._to_detail(lesson)

    async def update_lesson(self, lesson_id: int, fields: dict) -> LessonAdminDetail | None:
        lesson = await self.repository.update_lesson(lesson_id, fields)
        return self._to_detail(lesson) if lesson else None

    async def set_video(self, lesson_id: int, object_name: str, data: bytes, content_type: str) -> LessonAdminDetail | None:
        key = await self.video_provider.upload(object_name, data, content_type)
        return await self.update_lesson(lesson_id, {"video_url": key})

    async def set_sheetmusic(self, lesson_id: int, object_name: str, data: bytes, content_type: str) -> LessonAdminDetail | None:
        key = await self.sheetmusic_provider.upload(object_name, data, content_type)
        return await self.update_lesson(lesson_id, {"sheetmusic_url": key})

    def _to_detail(self, lesson) -> LessonAdminDetail:
        return LessonAdminDetail(
            id=lesson.id,
            lecture_id=lesson.lecture_id,
            title=lesson.title,
            length_sec=lesson.length_sec,
            text=lesson.text,
            lecture_ordering=lesson.lecture_ordering,
            session_type=lesson.session_type,
            sheetmusic_url=lesson.sheetmusic_url,
            video_url=lesson.video_url,
            sync_offset=lesson.sync_offset,
            subtitles=lesson.subtitles or [],
            playing_guide=lesson.playing_guide or [],
        )
```

- [ ] **Step 6: DI 등록** — `backend/app/containers/services.py`에 import 추가 + provider 추가

```python
from app.lesson.service import LessonService
```

```python
    lesson_service = providers.Factory(
        LessonService,
        repository=lesson_repository,
        video_provider=video_provider,
        sheetmusic_provider=sheetmusic_provider,
    )
```

- [ ] **Step 7: POST/PATCH 라우트** — `backend/app/lesson/view.py`에 추가 (subtitles/playing_guide는 `model_dump()`로 JSON 저장)

```python
from app.auth.access import superuser
from app.lesson.models import (
    CreateLessonBody,
    LessonAdminSchema,
    UpdateLessonBody,
)
from app.lesson.service import LessonService


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
    fields["subtitles"] = [s for s in fields.get("subtitles", [])]
    fields["playing_guide"] = [g for g in fields.get("playing_guide", [])]
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
```

> 주의: `body.model_dump()`는 `Subtitle`/`PlayingGuideStep`을 dict로 변환하므로 JSON 컬럼에 그대로 저장 가능. `create_lesson`의 fields 재대입은 불필요할 수 있으나 명시적으로 둔다.

- [ ] **Step 8: 통과 확인** — Run: `cd backend && uv run pytest tests/api/test_lesson_admin.py -v`  Expected: PASS (3 passed).

- [ ] **Step 9: 커밋**

```bash
git add backend/app/lesson backend/app/containers/services.py backend/tests/api/test_lesson_admin.py
git commit -m "✨ POST/PATCH /lesson 레슨 생성·편집 엔드포인트 + LessonService"
```

### Task 4: 업로드 엔드포인트 (video / sheetmusic / thumbnail)

**Files:**
- Modify: `backend/app/lesson/view.py` (video/sheetmusic 업로드)
- Modify: `backend/app/lecture/view.py` + service/repo (thumbnail 업로드)
- Test: `backend/tests/api/test_upload.py` (신규)

- [ ] **Step 1: 실패 테스트** — `backend/tests/api/test_upload.py`

```python
import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture, Lesson, User
import uuid

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def lecture_and_lesson(test_session: AsyncSession) -> None:
    now = datetime.datetime.now()
    artist = User(
        id=uuid.uuid4(), subscription_id=None, time_created=now, time_updated=now,
        email="a@a.com", nickname="a", hashed_password="p",
        is_artist=True, is_superuser=False, is_active=True,
    )
    async with test_session.begin():
        test_session.add(artist)
        await test_session.flush()
        test_session.add(
            Lecture(id=1, artist_id=None, thumbnail=None, title="L", description="d",
                    tags=None, length_sec=0, time_created=now, time_updated=now)
        )
        await test_session.flush()
        test_session.add(
            Lesson(id=1, title="L", artist_id=artist.id, lecture_id=1,
                   sheetmusic_url="", video_url="", text="", length_sec=0,
                   lecture_ordering=0, time_created=now, time_updated=now)
        )
    await test_session.commit()


async def test_upload_lesson_video(authorized_client_admin: AsyncClient, lecture_and_lesson):
    files = {"file": ("clip.mp4", b"binarydata", "video/mp4")}
    response = await authorized_client_admin.post("/lesson/1/video", files=files)
    assert response.status_code == 200
    assert response.json()["data"]["video_url"]


async def test_upload_lesson_sheetmusic(authorized_client_admin: AsyncClient, lecture_and_lesson):
    files = {"file": ("tab.musicxml", b"<score/>", "application/xml")}
    response = await authorized_client_admin.post("/lesson/1/sheetmusic", files=files)
    assert response.status_code == 200
    assert response.json()["data"]["sheetmusic_url"]


async def test_upload_video_forbidden_for_artist(authorized_client_artist: AsyncClient, lecture_and_lesson):
    files = {"file": ("clip.mp4", b"x", "video/mp4")}
    response = await authorized_client_artist.post("/lesson/1/video", files=files)
    assert response.status_code == 403
```

- [ ] **Step 2: 실패 확인** — Run: `cd backend && uv run pytest tests/api/test_upload.py -v`  Expected: FAIL.

- [ ] **Step 3: 업로드 라우트** — `backend/app/lesson/view.py`에 추가 (`from fastapi import File, UploadFile`)

```python
@app_router.post("/{lesson_id}/video", response_model=LessonAdminSchema)
@inject
async def upload_lesson_video(
    lesson_id: int,
    file: UploadFile = File(...),
    user: User = Depends(superuser),
    lesson_service: LessonService = Depends(
        Provide[ApplicationContainer.services.lesson_service]
    ),
):
    data = await file.read()
    object_name = f"lesson-{lesson_id}/{file.filename}"
    lesson = await lesson_service.set_video(
        lesson_id, object_name, data, file.content_type or "application/octet-stream"
    )
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return LessonAdminSchema(data=lesson)


@app_router.post("/{lesson_id}/sheetmusic", response_model=LessonAdminSchema)
@inject
async def upload_lesson_sheetmusic(
    lesson_id: int,
    file: UploadFile = File(...),
    user: User = Depends(superuser),
    lesson_service: LessonService = Depends(
        Provide[ApplicationContainer.services.lesson_service]
    ),
):
    data = await file.read()
    object_name = f"lesson-{lesson_id}/{file.filename}"
    lesson = await lesson_service.set_sheetmusic(
        lesson_id, object_name, data, file.content_type or "application/octet-stream"
    )
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return LessonAdminSchema(data=lesson)
```

- [ ] **Step 4: 통과 확인** — Run: `cd backend && uv run pytest tests/api/test_upload.py -v`  Expected: PASS.

- [ ] **Step 5: 커밋**

```bash
git add backend/app/lesson/view.py backend/tests/api/test_upload.py
git commit -m "✨ 레슨 동영상/악보 멀티파트 업로드 엔드포인트"
```

> 썸네일 업로드는 선택 사항. 1차 구현은 PATCH `/lecture/{id}`의 `thumbnail`(URL 문자열)로 충분. 이미지 업로드가 필요하면 후속 태스크로 `/lecture/{id}/thumbnail`을 video와 동일 패턴으로 추가.

---

## Phase 3 — 백엔드: 홈 큐레이션 모듈

### Task 5: home_curation 테이블 + 마이그레이션

**Files:**
- Modify: `backend/app/db/tables.py` (HomeCuration 모델)
- Create: `backend/app/db/migrations/versions/2026_06_14_add_home_curation.py`
- Test: (다음 태스크의 API 테스트로 검증)

- [ ] **Step 1: 모델 추가** — `backend/app/db/tables.py` 끝에

```python
class CurationSection(str, Enum):
    TRENDING = "TRENDING"
    NEW = "NEW"


class HomeCuration(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    section: Mapped[CurationSection] = mapped_column(
        Enum(CurationSection, name="curationsection"), nullable=False
    )
    lecture_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lecture.id"), nullable=False
    )
    ordering: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __tablename__ = "home_curation"
```

> `from enum import Enum`은 파일 상단에 이미 있는지 확인(없으면 추가). SQLAlchemy `Enum`은 이미 import됨.

- [ ] **Step 2: 마이그레이션 생성** — Run: `cd backend && uv run alembic revision --autogenerate -m "add home_curation"` 후 생성 파일을 `2026_06_14_add_home_curation.py`로 검토. (autogenerate가 어려우면 수동 작성: `op.create_table("home_curation", ...)` + enum 생성)

- [ ] **Step 3: 마이그레이션 적용 확인 (로컬 DB 있을 때)** — Run: `cd backend && uv run alembic upgrade head`  Expected: 에러 없음. (테스트는 SQLite + 메타데이터 create_all 사용하므로 별도)

- [ ] **Step 4: 커밋**

```bash
git add backend/app/db
git commit -m "✨ home_curation 테이블 + 마이그레이션"
```

### Task 6: curation 모듈 (GET 공개 / PUT superuser)

**Files:**
- Create: `backend/app/curation/__init__.py`, `models.py`, `repository.py`, `service.py`, `view.py`
- Modify: `backend/app/containers/services.py` (curation 등록)
- Modify: `backend/app/main.py` (라우터 + wiring)
- Modify: `backend/tests/conftest.py` (test_container.wire에 `app.curation.view` 추가)
- Test: `backend/tests/api/test_curation.py` (신규)

- [ ] **Step 1: 실패 테스트** — `backend/tests/api/test_curation.py`

```python
import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Lecture

pytest_plugins = ["tests.conftest", "tests.api.conftest"]


@pytest.fixture
async def lectures(test_session: AsyncSession) -> None:
    now = datetime.datetime.now()
    async with test_session.begin():
        test_session.add_all([
            Lecture(id=i, artist_id=None, thumbnail=None, title=f"L{i}",
                    description="d", tags=None, length_sec=0,
                    time_created=now, time_updated=now)
            for i in (1, 2, 3)
        ])
    await test_session.commit()


async def test_put_and_get_curation(authorized_client_admin: AsyncClient, client: AsyncClient, lectures):
    put = await authorized_client_admin.put(
        "/curation/TRENDING", json={"lecture_ids": [3, 1]}
    )
    assert put.status_code == 200

    get = await client.get("/curation")
    assert get.status_code == 200
    data = get.json()["data"]
    assert [item["id"] for item in data["TRENDING"]] == [3, 1]
    assert data["NEW"] == []


async def test_put_curation_forbidden_for_non_admin(authorized_client_artist: AsyncClient, lectures):
    response = await authorized_client_artist.put(
        "/curation/NEW", json={"lecture_ids": [1]}
    )
    assert response.status_code == 403
```

- [ ] **Step 2: 실패 확인** — Run: `cd backend && uv run pytest tests/api/test_curation.py -v`  Expected: FAIL (라우트 없음).

- [ ] **Step 3: models** — `backend/app/curation/models.py`

```python
from app.core.models import BaseSchema
from app.lecture.models import LectureInList


class SetCurationBody(BaseSchema):
    lecture_ids: list[int]


class CurationData(BaseSchema):
    TRENDING: list[LectureInList]
    NEW: list[LectureInList]


class GetCurationSchema(BaseSchema):
    data: CurationData
```

- [ ] **Step 4: repository** — `backend/app/curation/repository.py`

```python
import abc

from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from app.db import tables as tb
from app.db.session import SessionManager
from app.db.tables import CurationSection


class CurationRepository(abc.ABC):
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    async def set_section(self, section: CurationSection, lecture_ids: list[int]) -> None:
        async with self._session_manager.async_session() as session:
            await session.execute(
                delete(tb.HomeCuration).where(tb.HomeCuration.section == section)
            )
            for ordering, lecture_id in enumerate(lecture_ids):
                session.add(
                    tb.HomeCuration(section=section, lecture_id=lecture_id, ordering=ordering)
                )
            await session.commit()

    async def get_section_lectures(self, section: CurationSection) -> list[tb.Lecture]:
        async with self._session_manager.async_session() as session:
            rows = (
                (
                    await session.execute(
                        select(tb.HomeCuration)
                        .options(
                            joinedload(tb.HomeCuration.lecture)
                            .joinedload(tb.Lecture.artist),
                        )
                        .where(tb.HomeCuration.section == section)
                        .order_by(tb.HomeCuration.ordering)
                    )
                )
                .unique()
                .scalars()
                .all()
            )
            # lessons 로딩을 위해 lecture를 다시 selectin (간단화: lecture만 반환)
            return [row.lecture for row in rows]
```

> `HomeCuration.lecture` relationship 필요. `tables.py`의 `HomeCuration`에 추가:
> ```python
>     lecture: Mapped["Lecture"] = relationship("Lecture", lazy="selectin")
> ```
> 그리고 `Lecture.lessons`는 이미 `lazy="selectin"`이라 매핑에 사용 가능. `LectureRepository._map_to_lecture_list`를 재사용하기 어렵다면 service에서 직접 `LectureInList`로 변환.

- [ ] **Step 5: service** — `backend/app/curation/service.py`

```python
from app.curation.models import CurationData
from app.curation.repository import CurationRepository
from app.db.tables import CurationSection
from app.lecture.models import ArtistInfoInLecture, LectureInList
from app.lesson.models import LessonInLecture


class CurationService:
    def __init__(self, repository: CurationRepository) -> None:
        self.repository = repository

    async def set_section(self, section: CurationSection, lecture_ids: list[int]) -> None:
        await self.repository.set_section(section, lecture_ids)

    async def get_curation(self) -> CurationData:
        trending = await self.repository.get_section_lectures(CurationSection.TRENDING)
        new = await self.repository.get_section_lectures(CurationSection.NEW)
        return CurationData(
            TRENDING=[self._to_list_item(x) for x in trending],
            NEW=[self._to_list_item(x) for x in new],
        )

    def _to_list_item(self, lecture) -> LectureInList:
        artist = None
        if lecture.artist:
            artist = ArtistInfoInLecture(
                id=lecture.artist.id,
                nickname=lecture.artist.nickname,
                is_artist=lecture.artist.is_artist,
            )
        lessons = [
            LessonInLecture(
                id=l.id, title=l.title, length_sec=l.length_sec,
                lecture_ordering=l.lecture_ordering,
                time_created=l.time_created, time_updated=l.time_updated,
            )
            for l in lecture.lessons
        ]
        return LectureInList(
            id=lecture.id, thumbnail=lecture.thumbnail, title=lecture.title,
            artist=artist, lessons=lessons, description=lecture.description,
            tags=lecture.tags, length_sec=lecture.length_sec,
            lecture_count=lecture.lecture_count,
            time_created=lecture.time_created, time_updated=lecture.time_updated,
        )
```

- [ ] **Step 6: view** — `backend/app/curation/view.py`

```python
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.auth.access import superuser
from app.containers.application import ApplicationContainer
from app.curation.models import GetCurationSchema, SetCurationBody
from app.curation.service import CurationService
from app.db.tables import CurationSection

app_router = APIRouter()


@app_router.get("", response_model=GetCurationSchema)
@inject
async def get_curation(
    curation_service: CurationService = Depends(
        Provide[ApplicationContainer.services.curation_service]
    ),
):
    data = await curation_service.get_curation()
    return GetCurationSchema(data=data)


@app_router.put("/{section}")
@inject
async def set_curation(
    section: CurationSection,
    body: SetCurationBody,
    user=Depends(superuser),
    curation_service: CurationService = Depends(
        Provide[ApplicationContainer.services.curation_service]
    ),
):
    await curation_service.set_section(section, body.lecture_ids)
    return {"ok": True}
```

- [ ] **Step 7: DI 등록** — `backend/app/containers/services.py`

```python
from app.curation.repository import CurationRepository
from app.curation.service import CurationService
```

```python
    curation_repository = providers.Factory(
        CurationRepository,
        session_manager=database.session_manager,
    )
    curation_service = providers.Factory(
        CurationService,
        repository=curation_repository,
    )
```

- [ ] **Step 8: 라우터 + wiring** — `backend/app/main.py`

```python
from app.curation import view as curation_view
```
`create_container().wire(modules=[...])`에 `"app.curation.view"` 추가.
`api_router`에 추가:
```python
    api_router.include_router(curation_view.app_router, prefix="/curation", tags=["curation"])
```
그리고 `backend/tests/conftest.py:test_container`의 `container.wire(modules=[...])` 리스트에도 `"app.curation.view"` 추가.

- [ ] **Step 9: 통과 확인** — Run: `cd backend && uv run pytest tests/api/test_curation.py -v`  Expected: PASS (2 passed).

- [ ] **Step 10: 전체 백엔드 회귀** — Run: `cd backend && uv run pytest -q`  Expected: 전체 PASS.

- [ ] **Step 11: 커밋**

```bash
git add backend/app/curation backend/app/containers/services.py backend/app/main.py backend/app/db/tables.py backend/tests/conftest.py backend/tests/api/test_curation.py
git commit -m "✨ 홈 큐레이션 모듈 (GET 공개 / PUT superuser)"
```

---

## Phase 4 — OpenAPI 계약 재생성

### Task 7: 스냅샷 + 클라이언트 재생성

**Files:** `backend/openapi.json`, `frontend/src/lib/api/client/*`

- [ ] **Step 1: 재생성** — Run: `make gen-client`  (= `export-spec` + `yarn generate-client`)
- [ ] **Step 2: drift 검증** — Run: `make check-spec`  Expected: drift 없음(통과).
- [ ] **Step 3: 신규 함수명 확인** — `frontend/src/lib/api/client/services.gen.ts`에서 update lecture / create lesson / upload / curation 함수명을 확인하고 메모(프론트 태스크에서 사용).
- [ ] **Step 4: 커밋**

```bash
git add backend/openapi.json frontend/src/lib/api/client
git commit -m "🔧 OpenAPI 스냅샷 + 클라이언트 재생성 (admin 엔드포인트)"
```

---

## Phase 5 — 프론트: auth store 확장 + /admin 가드 + 진입점

### Task 8: auth store에 user 보관 + isAdmin

**Files:**
- Modify: `frontend/src/lib/features/auth/stores/auth.svelte.ts`
- Modify: `frontend/src/lib/features/auth/index.ts` (export)
- Modify: `frontend/src/routes/+layout.svelte` (user 저장)
- Test: `frontend/tests/unit/auth-store.test.ts` (신규, Vitest)

- [ ] **Step 1: 실패 테스트** — `frontend/tests/unit/auth-store.test.ts`

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { useAuth, setCurrentUser } from '$lib/features/auth/stores/auth.svelte'

describe('auth store', () => {
	beforeEach(() => setCurrentUser(null))

	it('비로그인 시 isAdmin은 false', () => {
		const auth = useAuth()
		expect(auth.isAuthenticated).toBe(false)
		expect(auth.isAdmin).toBe(false)
	})

	it('superuser 사용자 설정 시 isAdmin true', () => {
		setCurrentUser({ nickname: 'a', email: 'a@a.com', is_artist: false, is_superuser: true } as any)
		const auth = useAuth()
		expect(auth.isAuthenticated).toBe(true)
		expect(auth.isAdmin).toBe(true)
	})

	it('일반 사용자는 isAdmin false', () => {
		setCurrentUser({ nickname: 'b', email: 'b@b.com', is_artist: true, is_superuser: false } as any)
		expect(useAuth().isAdmin).toBe(false)
	})
})
```

- [ ] **Step 2: 실패 확인** — Run: `cd frontend && yarn vitest run tests/unit/auth-store.test.ts`  Expected: FAIL (`setCurrentUser` 없음).

- [ ] **Step 3: store 구현** — `frontend/src/lib/features/auth/stores/auth.svelte.ts`

```typescript
import type { UserRead } from '$lib/api'

let isAuthenticated = $state(false)
let currentUser = $state<UserRead | null>(null)

export function setIsAuthenticated(value: boolean) {
	isAuthenticated = value
}

export function setCurrentUser(user: UserRead | null) {
	currentUser = user
	isAuthenticated = user !== null
}

export function useAuth() {
	return {
		get isAuthenticated() {
			return isAuthenticated
		},
		get user() {
			return currentUser
		},
		get isAdmin() {
			return currentUser?.is_superuser === true
		}
	}
}
```

> `UserRead` 타입이 생성 클라이언트에 없으면 `$lib/api/client/types.gen.ts`의 실제 user 타입명으로 교체.

- [ ] **Step 4: export** — `frontend/src/lib/features/auth/index.ts`에 `setCurrentUser`, `useAuth` export 추가(기존 export 유지).

- [ ] **Step 5: 루트 레이아웃에서 user 저장** — `frontend/src/routes/+layout.svelte`의 `checkAuthentication` 수정

```typescript
	async function checkAuthentication() {
		try {
			const me = await usersCurrentUserUserMeGet()
			setCurrentUser(me)
		} catch {
			setCurrentUser(null)
		}
	}
```
(import에 `setCurrentUser` 추가; `setIsAuthenticated`는 내부에서 호출되므로 제거 가능)

- [ ] **Step 6: 통과 확인** — Run: `cd frontend && yarn vitest run tests/unit/auth-store.test.ts`  Expected: PASS.

- [ ] **Step 7: 타입체크** — Run: `cd frontend && yarn check`  Expected: 0 errors.

- [ ] **Step 8: 커밋**

```bash
git add frontend/src/lib/features/auth frontend/src/routes/+layout.svelte frontend/tests/unit/auth-store.test.ts
git commit -m "✨ auth store에 현재 사용자/isAdmin 보관"
```

### Task 9: /admin CSR 가드 레이아웃 + 진입점 링크

**Files:**
- Create: `frontend/src/routes/admin/+layout.ts` (`ssr=false`)
- Create: `frontend/src/routes/admin/+layout.svelte` (가드 + 네비)
- Create: `frontend/src/routes/admin/+page.svelte` (허브)
- Modify: `frontend/src/lib/components/layout/NavBar.svelte` (admin 링크)
- Test: `frontend/tests/routes/admin/guard.spec.ts` (Playwright)

- [ ] **Step 1: 가드 e2e 테스트** — `frontend/tests/routes/admin/guard.spec.ts` (기존 Playwright mock 패턴 참고: 기존 `tests/routes/**` 파일에서 `page.route('**/user/me', ...)` 형태 확인 후 일치시킬 것)

```typescript
import { test, expect } from '@playwright/test'

test('비로그인 사용자는 /admin 접근 시 /home으로 리다이렉트', async ({ page }) => {
	await page.route('**/user/me', (route) => route.fulfill({ status: 401, body: '{}' }))
	await page.goto('/admin')
	await expect(page).toHaveURL(/\/home/)
})

test('비관리자 사용자는 /admin 접근 시 /home으로 리다이렉트', async ({ page }) => {
	await page.route('**/user/me', (route) =>
		route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({ nickname: 'u', email: 'u@u.com', is_artist: false, is_superuser: false })
		})
	)
	await page.goto('/admin')
	await expect(page).toHaveURL(/\/home/)
})

test('관리자는 /admin 진입 가능', async ({ page }) => {
	await page.route('**/user/me', (route) =>
		route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({ nickname: 'admin', email: 'a@a.com', is_artist: false, is_superuser: true })
		})
	)
	await page.goto('/admin')
	await expect(page.getByTestId('admin-hub')).toBeVisible()
})
```

- [ ] **Step 2: 실패 확인** — Run: `cd frontend && yarn playwright test tests/routes/admin/guard.spec.ts`  Expected: FAIL (라우트 없음).

- [ ] **Step 3: CSR 강제** — `frontend/src/routes/admin/+layout.ts`

```typescript
export const ssr = false
```

- [ ] **Step 4: 가드 레이아웃** — `frontend/src/routes/admin/+layout.svelte`

```svelte
<script lang="ts">
	import { onMount } from 'svelte'
	import { goto } from '$app/navigation'
	import { waitForApiInit, usersCurrentUserUserMeGet } from '$lib/api'
	import { setCurrentUser, useAuth } from '$lib/features/auth'
	import type { Snippet } from 'svelte'

	let { children }: { children: Snippet } = $props()
	let checked = $state(false)
	const auth = useAuth()

	onMount(async () => {
		await waitForApiInit()
		try {
			const me = await usersCurrentUserUserMeGet()
			setCurrentUser(me)
		} catch {
			setCurrentUser(null)
		}
		if (!auth.isAdmin) {
			goto('/home', { replaceState: true })
			return
		}
		checked = true
	})
</script>

{#if checked}
	<div class="min-h-screen bg-black text-white px-6 py-20 max-w-[1024px] mx-auto" data-testid="admin-shell">
		<nav class="flex gap-4 mb-8 text-sm">
			<a href="/admin/lectures" class="hover:text-[#FF5C16]">렉처</a>
			<a href="/admin/curation" class="hover:text-[#FF5C16]">홈 큐레이션</a>
		</nav>
		{@render children()}
	</div>
{:else}
	<div class="min-h-screen bg-black" data-testid="admin-loading"></div>
{/if}
```

- [ ] **Step 5: 허브 페이지** — `frontend/src/routes/admin/+page.svelte`

```svelte
<script lang="ts">
</script>

<div data-testid="admin-hub" class="flex flex-col gap-4">
	<h1 class="text-2xl font-bold">관리자</h1>
	<a href="/admin/lectures" class="underline">렉처 생성/편집</a>
	<a href="/admin/curation" class="underline">홈 큐레이션 선정</a>
</div>
```

- [ ] **Step 6: NavBar 진입점** — `frontend/src/lib/components/layout/NavBar.svelte` 데스크탑 메뉴에 admin 링크(관리자만)

```svelte
	import { useAuth } from '$lib/features/auth'
	const auth = useAuth()
```
데스크탑 메뉴 div 내부에 추가:
```svelte
	{#if auth.isAdmin}
		<a href="/admin" data-testid="nav-admin"
			class="h-[50px] w-[88px] flex items-center justify-center text-[13px] font-bold text-[#FF5C16] whitespace-nowrap">
			관리자
		</a>
	{/if}
```

- [ ] **Step 7: 통과 확인** — Run: `cd frontend && yarn playwright test tests/routes/admin/guard.spec.ts`  Expected: PASS (3 passed).

- [ ] **Step 8: 커밋**

```bash
git add frontend/src/routes/admin frontend/src/lib/components/layout/NavBar.svelte frontend/tests/routes/admin
git commit -m "✨ /admin CSR 가드 + 관리자 진입점"
```

---

## Phase 6 — 프론트: 자막 파서 + admin 페이지들

### Task 10: SRT/VTT 자막 파서 (유닛)

**Files:**
- Create: `frontend/src/lib/features/admin/utils/subtitle-parser.ts`
- Test: `frontend/tests/unit/subtitle-parser.test.ts`

- [ ] **Step 1: 실패 테스트** — `frontend/tests/unit/subtitle-parser.test.ts`

```typescript
import { describe, it, expect } from 'vitest'
import { parseSubtitles } from '$lib/features/admin/utils/subtitle-parser'

describe('parseSubtitles', () => {
	it('SRT를 timestamp_ms/text 배열로 변환', () => {
		const srt = `1\n00:00:00,000 --> 00:00:02,000\n안녕하세요\n\n2\n00:00:02,500 --> 00:00:04,000\n반갑습니다`
		expect(parseSubtitles(srt)).toEqual([
			{ timestamp_ms: 0, text: '안녕하세요' },
			{ timestamp_ms: 2500, text: '반갑습니다' }
		])
	})

	it('WEBVTT 헤더와 점(.) 밀리초 처리', () => {
		const vtt = `WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nhello`
		expect(parseSubtitles(vtt)).toEqual([{ timestamp_ms: 1000, text: 'hello' }])
	})

	it('여러 줄 텍스트는 공백으로 합침', () => {
		const srt = `1\n00:00:00,000 --> 00:00:01,000\na\nb`
		expect(parseSubtitles(srt)).toEqual([{ timestamp_ms: 0, text: 'a b' }])
	})

	it('빈 입력은 빈 배열', () => {
		expect(parseSubtitles('')).toEqual([])
	})
})
```

- [ ] **Step 2: 실패 확인** — Run: `cd frontend && yarn vitest run tests/unit/subtitle-parser.test.ts`  Expected: FAIL.

- [ ] **Step 3: 구현** — `frontend/src/lib/features/admin/utils/subtitle-parser.ts`

```typescript
export interface SubtitleRow {
	timestamp_ms: number
	text: string
}

function toMs(stamp: string): number {
	const m = stamp.trim().match(/(\d{2}):(\d{2}):(\d{2})[.,](\d{3})/)
	if (!m) return 0
	const [, h, min, s, ms] = m
	return ((+h * 60 + +min) * 60 + +s) * 1000 + +ms
}

export function parseSubtitles(input: string): SubtitleRow[] {
	const text = input.replace(/^WEBVTT.*$/m, '').trim()
	if (!text) return []
	const blocks = text.split(/\n\s*\n/)
	const rows: SubtitleRow[] = []
	for (const block of blocks) {
		const lines = block.split('\n').map((l) => l.trim()).filter(Boolean)
		const cueIndex = lines.findIndex((l) => l.includes('-->'))
		if (cueIndex === -1) continue
		const start = lines[cueIndex].split('-->')[0]
		const body = lines.slice(cueIndex + 1).join(' ').trim()
		if (!body) continue
		rows.push({ timestamp_ms: toMs(start), text: body })
	}
	return rows
}
```

- [ ] **Step 4: 통과 확인** — Run: `cd frontend && yarn vitest run tests/unit/subtitle-parser.test.ts`  Expected: PASS (4 passed).

- [ ] **Step 5: 커밋**

```bash
git add frontend/src/lib/features/admin
git commit -m "✨ SRT/VTT 자막 파서"
```

### Task 11: 렉처 관리 페이지 (목록/생성/편집 + 레슨 목록)

**Files:**
- Create: `frontend/src/routes/admin/lectures/+page.svelte` (목록 + 생성 폼)
- Create: `frontend/src/routes/admin/lectures/[id]/+page.svelte` (속성 편집 + 레슨 목록 링크)
- Test: `frontend/tests/routes/admin/lectures.spec.ts`

- [ ] **Step 1: e2e 테스트(핵심 흐름, 백엔드 mock)** — admin user로 `/user/me` mock + `GET /lecture`, `POST /lecture`, `PATCH /lecture/{id}` mock. 생성 폼 제출 → 목록 갱신, 편집 저장 → 성공 토스트/필드 반영 검증. (기존 `tests/routes/**`의 mock 헬퍼 패턴을 따른다.)

- [ ] **Step 2: 실패 확인** — Run: `cd frontend && yarn playwright test tests/routes/admin/lectures.spec.ts`  Expected: FAIL.

- [ ] **Step 3: 목록/생성 페이지 구현** — `frontend/src/routes/admin/lectures/+page.svelte`
  - `onMount`에서 `waitForApiInit()` 후 `getLecturesLectureGet({})`로 목록 로드(`$state` 배열).
  - 생성 폼: title/description 입력 → `createLectureLecturePost(...)`(Task7에서 확인한 함수명) → 목록에 prepend.
  - 각 렉처에 `/admin/lectures/{id}` 편집 링크. flowbite-svelte `Input`/`Button`/`Table` 사용. `data-testid` 부착(`lecture-title-input`, `create-lecture-btn`, `lecture-row`).

- [ ] **Step 4: 편집 페이지 구현** — `frontend/src/routes/admin/lectures/[id]/+page.svelte`
  - `$page.params.id`로 `getLectureLectureLectureIdGet`로 상세 로드.
  - 편집 폼: title/description/tags(LectureType select + DifficultyLevel select)/thumbnail(URL) → `updateLectureLectureLectureIdPatch({ ..., requestBody })` 저장.
  - 소속 레슨 목록 렌더 + `/admin/lessons/new?lectureId={id}` 추가 링크, 각 레슨 `/admin/lessons/{lessonId}` 편집 링크.
  - `data-testid`: `edit-title-input`, `save-lecture-btn`, `lesson-item`, `add-lesson-link`.

- [ ] **Step 5: 통과 확인** — Run: `cd frontend && yarn playwright test tests/routes/admin/lectures.spec.ts`  Expected: PASS.

- [ ] **Step 6: 커밋**

```bash
git add frontend/src/routes/admin/lectures frontend/tests/routes/admin/lectures.spec.ts
git commit -m "✨ admin 렉처 목록/생성/편집 페이지"
```

### Task 12: 레슨 생성/편집 페이지 (업로드 + 자막 표 편집)

**Files:**
- Create: `frontend/src/routes/admin/lessons/new/+page.svelte`
- Create: `frontend/src/routes/admin/lessons/[id]/+page.svelte`
- Create: `frontend/src/lib/features/admin/components/SubtitleEditor.svelte`
- Create: `frontend/src/lib/features/admin/components/FileUploadField.svelte`
- Test: `frontend/tests/routes/admin/lessons.spec.ts`

- [ ] **Step 1: e2e 테스트** — admin mock + `POST /lesson`(new), `PATCH /lesson/{id}`, `POST /lesson/{id}/video`, `POST /lesson/{id}/sheetmusic` mock. 흐름: 새 레슨 생성(title/session_type/ordering) → 저장 성공; 자막 파일 업로드 → 표에 행 렌더 → 저장 시 `PATCH`에 subtitles 전달; 동영상 파일 선택 → 업로드 호출. `setInputFiles`로 파일 선택 시뮬레이션.

- [ ] **Step 2: 실패 확인** — Run: `cd frontend && yarn playwright test tests/routes/admin/lessons.spec.ts`  Expected: FAIL.

- [ ] **Step 3: SubtitleEditor 컴포넌트** — `frontend/src/lib/features/admin/components/SubtitleEditor.svelte`
  - props: `rows: SubtitleRow[]` (bindable). `<input type=file accept=".srt,.vtt">` → `parseSubtitles(text)`로 채움.
  - 표: 각 행 timestamp_ms(number input) + text(text input) 편집, 행 추가/삭제 버튼.
  - `data-testid`: `subtitle-file`, `subtitle-row`, `subtitle-text-{i}`.

- [ ] **Step 4: FileUploadField 컴포넌트** — `frontend/src/lib/features/admin/components/FileUploadField.svelte`
  - props: `label`, `accept`, `onUpload: (file: File) => Promise<void>`. 파일 선택 → 업로드 버튼 → 진행/완료 상태 표시.
  - `data-testid`: `upload-input`, `upload-btn`, `upload-status`.

- [ ] **Step 5: 새 레슨 페이지** — `frontend/src/routes/admin/lessons/new/+page.svelte`
  - 쿼리 `lectureId` 읽기. 폼: title/session_type(select PLAY/TALK/JAM/BASIC/SHEET)/lecture_ordering/length_sec/text. 저장 → `createLessonLessonPost({ requestBody: { lecture_id, ... } })` → 성공 시 `/admin/lessons/{id}`로 이동.

- [ ] **Step 6: 레슨 편집 페이지** — `frontend/src/routes/admin/lessons/[id]/+page.svelte`
  - 상세 로드(레슨 admin GET이 없으므로 편집 진입은 생성 직후 상태 전달 또는 `session` 상세 재사용 대신, 간단히 `lectures/[id]`에서 넘긴 데이터로 초기화하거나 `GET /lesson/{id}`가 필요하면 후속). 1차: 생성 직후 이동 + 클라이언트 상태로 편집.
  - 동영상 업로드(`FileUploadField` → `uploadLessonVideoLessonLessonIdVideoPost` multipart), 악보 업로드(`...Sheetmusic...`), 자막(`SubtitleEditor`) → 저장 시 `updateLessonLessonLessonIdPatch({ requestBody: { subtitles, ... } })`.
  - **multipart 업로드 주의**: 생성 클라이언트가 `File`을 받는지 확인. 필요 시 `axios`로 `FormData` 직접 전송(`$lib/api/config`의 baseURL 사용).

> 참고: 편집 페이지 초기 로드를 위해 `GET /lesson/{id}`(admin)가 있으면 UX가 깔끔하다. 범위를 줄이려면 1차는 생성→편집 연속 흐름으로 충분. 필요 시 백엔드에 `GET /lesson/{id}`(superuser, LessonAdminDetail) 추가를 후속 태스크로.

- [ ] **Step 7: 통과 확인** — Run: `cd frontend && yarn playwright test tests/routes/admin/lessons.spec.ts`  Expected: PASS.

- [ ] **Step 8: 커밋**

```bash
git add frontend/src/routes/admin/lessons frontend/src/lib/features/admin/components frontend/tests/routes/admin/lessons.spec.ts
git commit -m "✨ admin 레슨 생성/편집 + 업로드 + 자막 편집"
```

### Task 13: 홈 큐레이션 선정 페이지 + 홈 연동

**Files:**
- Create: `frontend/src/routes/admin/curation/+page.svelte`
- Modify: `frontend/src/routes/home/+page.svelte` (curation 사용)
- Test: `frontend/tests/routes/admin/curation.spec.ts`

- [ ] **Step 1: e2e 테스트** — admin mock + `GET /lecture`(후보), `GET /curation`, `PUT /curation/{section}` mock. 흐름: 후보에서 렉처를 TRENDING/NEW에 추가 → 순서 위/아래 이동 → 저장 시 `PUT`에 `lecture_ids` 순서대로 전달.

- [ ] **Step 2: 실패 확인** — Run: `cd frontend && yarn playwright test tests/routes/admin/curation.spec.ts`  Expected: FAIL.

- [ ] **Step 3: curation 페이지 구현** — `frontend/src/routes/admin/curation/+page.svelte`
  - `getCurationCurationGet`로 두 섹션 초기 로드, `getLecturesLectureGet`로 후보 목록.
  - 섹션별 `$state<number[]>` (lecture_ids). 후보에서 추가/제거, 위/아래 이동 버튼.
  - 저장: 각 섹션 `setCurationCurationSectionPut({ section, requestBody: { lecture_ids } })`.
  - `data-testid`: `section-TRENDING`, `section-NEW`, `add-to-{section}-{id}`, `move-up-{i}`, `save-{section}-btn`.

- [ ] **Step 4: 홈 연동** — `frontend/src/routes/home/+page.svelte`

```svelte
	import { getCurationCurationGet, waitForApiInit } from '$lib/api'
	// ...
	async function fetchLectures() {
		await waitForApiInit()
		try {
			const res = await getCurationCurationGet()
			recommendedLectures = res.data?.TRENDING ?? []
			newLectures = res.data?.NEW ?? []
		} catch (error) {
			console.error('Failed to fetch curation:', error)
			recommendedLectures = []
			newLectures = []
		}
	}
```
(함수명은 Task7에서 확인한 실제 생성 함수명으로 맞춘다.)

- [ ] **Step 5: 통과 확인** — Run: `cd frontend && yarn playwright test tests/routes/admin/curation.spec.ts`  Expected: PASS.

- [ ] **Step 6: 홈 회귀** — 기존 home 관련 e2e가 `getLecturesLectureGet`를 mock한다면 `getCurationCurationGet` mock으로 갱신 필요. Run: `cd frontend && yarn playwright test tests/routes/` 영향 범위 확인 후 수정.

- [ ] **Step 7: 커밋**

```bash
git add frontend/src/routes/admin/curation frontend/src/routes/home frontend/tests/routes/admin/curation.spec.ts
git commit -m "✨ admin 홈 큐레이션 선정 페이지 + 홈 연동"
```

---

## Phase 7 — 통합 검증

### Task 14: 전체 테스트 + 린트 + 타입체크 + 계약

- [ ] **Step 1: 백엔드 전체** — Run: `make test-be`  Expected: 전체 PASS.
- [ ] **Step 2: 계약 drift** — Run: `make check-spec`  Expected: 통과.
- [ ] **Step 3: 프론트 유닛** — Run: `cd frontend && yarn vitest run`  Expected: 전체 PASS.
- [ ] **Step 4: 프론트 e2e** — Run: `cd frontend && yarn playwright test`  Expected: 전체 PASS.
- [ ] **Step 5: 타입체크 + 린트** — Run: `make check && make lint`  Expected: 0 errors.
- [ ] **Step 6: 정리 커밋(필요 시)** — 포맷: `make format` 후 변경 있으면 커밋.

### Task 15: PR 생성

- [ ] **Step 1: 푸시** — Run: `git push -u origin cc/sharp-bassi-b4ef61`
- [ ] **Step 2: PR 생성** — `gh pr create`로 base `main`, 본문에 요약/테스트 결과/스크린샷 안내. 마지막 줄에 Claude Code 생성 표기.

---

## Self-Review (작성자 점검 결과)

- **스펙 커버리지**: ① 렉처 생성/편집 → Task 1, 11. ② 레슨 생성/업로드/자막/악보 → Task 3·4·10·12. ③ 홈 큐레이션 선정 → Task 5·6·13. /admin 가드+진입점 축소 → Task 8·9. 계약 → Task 7. 모두 매핑됨.
- **타입 일관성**: `LessonAdminDetail`/`LessonAdminSchema`(data 래핑), `CurationData(TRENDING/NEW)`, `SubtitleRow{timestamp_ms,text}`가 백엔드 `Subtitle`과 일치. 함수명은 codegen 후 Task7에서 확정하도록 명시.
- **placeholder**: 프론트 페이지 구현 스텝은 컴포넌트/호출/테스트id를 구체화했고, 정확한 생성 함수명은 codegen 산출물 의존이라 Task7 확인 지점을 박아둠(불가피한 의존성). 백엔드는 전부 실제 코드 제공.
- **알려진 의존/리스크**: (a) 생성 클라이언트의 multipart 지원 여부 → Task12 Step6에서 axios/FormData 폴백 명시. (b) 레슨 편집 초기 로드용 `GET /lesson/{id}`(admin) 부재 → 1차는 생성→편집 연속 흐름, 필요 시 후속. (c) Playwright home 기존 mock 갱신 → Task13 Step6.
