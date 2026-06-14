# Sessionary Admin 페이지 설계

- 작성일: 2026-06-14
- 상태: 승인됨 (설계 합의 완료)
- 전달 단위: 단일 브랜치 → PR 1개 (main 직접 push 금지)

## 1. 목표

`/admin` 서브라우트에 관리자 전용 페이지를 구현한다. 포함 기능:

1. **렉처 생성/편집** — 속성(title, description, tags, thumbnail) 편집
2. **레슨 생성/편집** — 동영상 클립 업로드, 자막 업로드(표 미세편집), TAB(musicxml/gp) 업로드
3. **홈 큐레이션 선정** — `요즘 많이 보는 렉처` / `새로운 렉처` 섹션 수동 선정

요구사항:
- 인증정보가 없거나 admin이 아니면 `/home`으로 리다이렉트
- admin 진입점은 `/home`에서 로그인 → admin 페이지 이동으로 축소

## 2. 현재 코드베이스 사실 (Ground truth)

- **도메인 계층**: `Lecture`(곡/주제) → `Lesson`(개별 학습 단위, `lecture_id` FK). 백엔드 "세션 상세"(`GET /session/{id}`)는 사실 `Lesson` 행을 조회하는 뷰다. 즉 사용자 표현의 "레슨 생성" = `Lesson` 레코드 생성.
- **`Lesson` 컬럼** (`backend/app/db/tables.py`): `title`, `artist_id`, `lecture_id`, `length_sec`, `sheetmusic_url`, `video_url`, `text`, `lecture_ordering`, `session_type`(Enum PLAY/TALK/JAM/BASIC/SHEET), `subtitles`(JSON), `playing_guide`(JSON), `sync_offset`.
- **`Lecture` 컬럼**: `artist_id`, `thumbnail`, `title`, `description`, `tags`(TagsType=JSON 직렬화된 `(LectureType, DifficultyLevel)`), `length_sec`, `lecture_count`.
- **권한**: `User.is_superuser` 존재. `app/auth/access.py`에 `superuser` 디펜던시 존재, 이미 `POST /lecture`를 보호 중.
- **업로드 부재**: `VideoProvider` / `SheetmusicProvider`는 읽기(`get_video_url`/`get_url`)만 있고 업로드 메서드 없음.
- **홈 큐레이션 부재**: `LectureService.get_recommended`는 `fetch_lectures`(time_updated desc)만 호출. "요즘 많이 보는"/"새로운" 구분 개념이 백엔드에 없음. 홈(`/home/+page.svelte`)은 두 섹션을 동일한 `getLecturesLectureGet` 결과로 채움.
- **프론트 인증 상태**: `auth.svelte.ts` 스토어는 `isAuthenticated`(boolean)만 보관. 루트 `+layout.svelte`가 `onMount`에서 `/user/me` 호출 후 boolean만 설정(사용자 객체 폐기). `UserRead`에는 `is_superuser` 포함됨.
- **API 계약**: 스냅샷 기반. `backend/openapi.json` 커밋 → `make gen-client`(`yarn openapi-ts`)로 `frontend/src/lib/api/client/*` 재생성. CI `make check-spec`가 drift 검증.
- **스토리지**: dev=MinIO, prod=Cloudflare. 버킷 `videos`. (`infra/dev` docker compose)
- **프론트 스택**: SvelteKit + Svelte 5 Runes, flowbite-svelte, OpenAPI 생성 클라이언트(axios). 테스트: Vitest(unit) + Playwright(e2e, 백엔드 page.route mock).
- **백엔드 스택**: FastAPI + dependency-injector + SQLAlchemy(async). 테스트: pytest + SQLite(aiosqlite).

## 3. 결정 사항 (확정)

| 항목 | 결정 |
|------|------|
| 전달 단위 | 한 번에 전체 구현 → PR 1개 |
| 홈 큐레이션 저장 | 큐레이션 테이블 + 두 섹션 수동 선정 |
| 업로드 흐름 | 백엔드 멀티파트 업로드 → 스토리지 저장 (dev=MinIO 우선) |
| 자막/악보 입력 | 파일 업로드 + 표 미세편집(자막), musicxml은 업로드 전용 |

## 4. 아키텍처

### 4.1 권한 & 진입

- admin = `is_superuser`. 모든 admin 쓰기 엔드포인트는 `superuser` 디펜던시로 보호.
- **auth store 확장**: `user: UserRead | null` 보관 + `isAdmin` 파생. 루트 `+layout.svelte`의 `checkAuthentication()`이 `/user/me` 결과를 스토어에 저장.
- **진입점**: NavBar(또는 `/home`)에 `is_superuser`일 때만 "관리자" 링크 노출.
- **`/admin` 가드**: `/admin` 그룹을 CSR 전용(`export const ssr = false`)으로 설정. `/admin/+layout.svelte`(또는 `+layout.ts`)에서 `/user/me` 확인 → 미인증 또는 `!is_superuser`면 `goto('/home', { replaceState: true })`. 확인 완료 전엔 콘텐츠 미렌더(로딩 표시). 기존 CSR 쿠키 인증 패턴과 일관.

### 4.2 백엔드 변경

도메인 모듈 구조를 유지하고 각 도메인에 superuser-gated 쓰기 엔드포인트를 추가한다. 홈 큐레이션은 신규 `curation` 모듈로 분리한다.

**(a) Lecture 편집** (`app/lecture/`)
- `PATCH /lecture/{id}` (superuser): `title`/`description`/`tags`/`thumbnail` 부분 편집. body는 모두 optional.
- `POST /lecture/{id}/thumbnail` (multipart, superuser): 이미지 업로드 → 스토리지 → `thumbnail` 기록.
- 기존 `POST /lecture` 유지.

**(b) Lesson 생성/편집** (`app/lesson/`)
- `POST /lesson` (superuser): `lecture_id`, `title`, `session_type`, `lecture_ordering`, `length_sec`, `text`, `sync_offset`, `subtitles`, `playing_guide`.
- `PATCH /lesson/{id}` (superuser): 부분 업데이트 — 특히 `subtitles`(JSON), `playing_guide`(JSON), `session_type`, `lecture_ordering`, `sync_offset`, `text`.
- `POST /lesson/{id}/video` (multipart, superuser): 동영상 클립 → `VideoProvider.upload` → `video_url` 기록.
- `POST /lesson/{id}/sheetmusic` (multipart, superuser): `.musicxml`/`.gp` → `SheetmusicProvider.upload` → `sheetmusic_url` 기록.
- 자막: 별도 파일 엔드포인트 없이 프론트에서 SRT/VTT 파싱 → 표 편집 → `PATCH /lesson`의 `subtitles`로 저장.

**(c) Provider 업로드 메서드**
- `VideoProvider.upload(object_name, data, content_type) -> str` 추상 메서드 추가. `MinIOVideoProvider`는 `put_object` 구현. `CloudflareVideoProvider`는 이번 범위에서 `NotImplementedError` 스텁(읽기는 기존대로).
- `SheetmusicProvider.upload(...)` 동일 패턴. `sheetmusic/minio.py` 구현.
- 썸네일: MinIO `images` 버킷(또는 동일 클라이언트 재사용)으로 업로드.

**(d) 홈 큐레이션** (신규 `app/curation/`)
- 신규 테이블 `home_curation`: `id`(PK), `section`(Enum: `TRENDING`='요즘 많이 보는', `NEW`='새로운'), `lecture_id`(FK→lecture.id), `ordering`(int). 섹션별 정렬된 렉처 목록.
- Alembic 마이그레이션 추가.
- `GET /curation` (public): 두 섹션의 렉처 목록(LectureInList 형태) 반환.
- `PUT /curation/{section}` (superuser): 섹션의 `lecture_id` 목록(순서 포함)으로 전체 교체.

**(e) 라우터 등록**: `app/main.py`에 `curation_view.app_router` 추가(`/curation`), `container.wire`에 `app.curation.view` 등록.

**(f) 계약 재생성**: 엔드포인트 추가 후 `make gen-client` → `backend/openapi.json` + `frontend/src/lib/api/client/*` 재생성·커밋. `make check-spec` 통과 확인.

### 4.3 프론트 `/admin` 페이지 (CSR 그룹, flowbite-svelte)

- `/admin` — 허브: 세 기능 링크.
- `/admin/lectures` — 렉처 목록 + 생성 폼.
- `/admin/lectures/[id]` — 렉처 속성 편집(title/description/tags/thumbnail 업로드) + 소속 레슨 목록(추가/이동).
- `/admin/lessons/new?lectureId=` & `/admin/lessons/[id]` — 레슨 생성/편집:
  - 동영상 클립 업로드(진행률), 자막(SRT/VTT 업로드 → 표 편집 → 저장), TAB(musicxml/gp 업로드),
  - `session_type` 선택, `lecture_ordering`, `length_sec`, `text`, `playing_guide`, `sync_offset`.
- `/admin/curation` — 두 섹션('요즘 많이 보는'/'새로운')에 렉처 검색·추가·순서 정렬(위/아래)·저장.
- 홈 `/home/+page.svelte`: 기존 "둘 다 같은 목록" → `GET /curation` 기반으로 두 섹션 분리.

공통 레이아웃 `/admin/+layout.svelte`: 가드 + admin 네비게이션 쉘.

### 4.4 자막 SRT/VTT 파서 (프론트 유닛)

- 입력: `.srt` 또는 `.vtt` 텍스트.
- 출력: `{ timestamp_ms: number, text: string }[]` (백엔드 `Subtitle` 스키마와 일치).
- 위치: `frontend/src/lib/features/` 하위 유틸. Vitest 단위 테스트 대상.

## 5. 테스트 전략

**백엔드** (pytest/SQLite, `tests/api/` — 기존 `test_lecture.py` 패턴):
- `PATCH /lecture/{id}` 속성 업데이트 + 비-superuser 403
- `POST /lesson`, `PATCH /lesson/{id}` (subtitles/playing_guide 포함) + 권한
- 업로드 엔드포인트: provider mock으로 `video_url`/`sheetmusic_url` 기록 검증 + 권한
- `GET /curation`(public) / `PUT /curation/{section}`(superuser) 라운드트립 + 권한

**프론트**:
- Vitest: SRT/VTT 파서, curation 순서(위/아래 이동) 로직
- Playwright: `/admin` 가드 리다이렉트(비-admin → `/home`), 렉처 생성·레슨 폼·curation 저장 흐름 (백엔드 mock)

## 6. 마이그레이션 / 주의사항

- Alembic 마이그레이션으로 `home_curation` 테이블 추가.
- 업로드: 확장자/용량 검증, multipart 처리. 비디오/악보 prod(Cloudflare) 업로드는 이번 범위 스텁, dev(MinIO) 동작 보장.
- musicxml은 업로드 전용(표 미세편집은 자막에만 적용).
- API 계약 drift 방지를 위해 백엔드 변경 후 반드시 client 재생성·커밋.

## 7. 비범위 (Out of scope)

- Cloudflare Stream 업로드(tus/direct upload) 구현 — 추후 별도 작업.
- 비주얼 악보 에디터(musicxml 시각 편집).
- 렉처/레슨 삭제(요구사항에 없음) — 필요 시 후속.
- 조회수 기반 자동 추천 알고리즘(수동 선정으로 대체).
