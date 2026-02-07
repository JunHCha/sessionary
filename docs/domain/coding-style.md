# Coding Style

## 기술 스택

| 영역 | 기술 | 버전 |
|------|------|------|
| **Backend 언어** | Python | >=3.11 |
| **Backend 프레임워크** | FastAPI | 0.115.1+ |
| **ORM** | SQLAlchemy | 2.0.29+ |
| **DB 마이그레이션** | Alembic | - |
| **DB** | PostgreSQL | asyncpg 드라이버 |
| **인증** | fastapi-users | 13+ (Redis 세션) |
| **DI** | dependency-injector | 4.41.0+ |
| **Backend 테스트** | pytest + pytest-asyncio | 7.4.0+ |
| **Backend 린터** | Ruff | 0.14.0+ |
| **Frontend 언어** | TypeScript | 5.x |
| **Frontend 프레임워크** | SvelteKit + Svelte 5 | 2.50.0+ / 5.48.0+ |
| **빌드 도구** | Vite | 6.0.0+ |
| **CSS** | Tailwind CSS | 3.4.14+ |
| **UI 라이브러리** | Flowbite Svelte | 1.30.1+ |
| **HTTP 클라이언트** | Axios | 1.12.0+ |
| **비디오** | HLS.js | 1.6.15+ |
| **Frontend 유닛 테스트** | Vitest | 4.0.15+ |
| **Frontend E2E 테스트** | Playwright | 1.44.1+ |
| **Frontend 린터** | ESLint (flat config) | 8.52.0 |
| **Frontend 포매터** | Prettier | 3.4.2 |
| **패키지 매니저** | Yarn (frontend), Poetry (backend) | - |
| **배포** | Fly.io (컨테이너) | - |
| **Node** | Node.js | 20 |

## 코딩 규칙

### 네이밍 컨벤션

#### Backend (Python)
- **파일/모듈**: `snake_case` (예: `lecture_service.py`)
- **클래스**: `PascalCase` (예: `LectureService`)
- **함수/변수**: `snake_case` (예: `get_lecture_detail`)
- **상수**: `UPPER_SNAKE_CASE` (예: `COOKIE_NAME`)
- **DB 모델 필드**: `snake_case` (예: `time_created`)

#### Frontend (TypeScript/Svelte)
- **파일**: `PascalCase` for 컴포넌트 (예: `VideoPlayer.svelte`), `kebab-case` for 라우트
- **변수/함수**: `camelCase` (예: `loadSessionDetail`)
- **타입/인터페이스**: `PascalCase` (예: `SessionDetailData`)
- **상수**: `UPPER_SNAKE_CASE` (예: `COOKIE_NAME`)
- **CSS 클래스**: Tailwind 유틸리티 클래스 직접 사용

### 패턴

#### Backend
- **Layered Architecture**: View → Service → Repository
- **의존성 주입**: `dependency-injector`로 컨테이너 기반 DI
- **비동기**: 모든 DB/외부 호출에 `async/await`
- **Pydantic 스키마**: API 요청/응답 검증

#### Frontend
- **Feature-based 구조**: `lib/features/{도메인}/` 하위에 components, services, types, utils
- **Svelte 5 Runes**: `$state`, `$derived`, `$effect`, `$props` 사용
- **OpenAPI 코드 생성**: 백엔드 스키마에서 타입 자동 생성
- **data-testid 속성**: 테스트 가능한 컴포넌트에 부착

### 금지 사항

- JWT 토큰 사용 금지 (Redis 세션 쿠키 사용)
- Svelte 4 스타일 반응성 (reactive declarations `$:`) 금지 → Runes 사용
- `any` 타입 사용 최소화
- 환경변수 값을 코드에 하드코딩 금지

## 린터/포매터 설정

### Backend (Ruff)

```toml
# pyproject.toml
[tool.ruff]
select = ["I"]  # Import sorting

[tool.ruff.isort]
combine-as-imports = true
force-sort-within-sections = true
known-first-party = ["app"]
split-on-trailing-comma = true
```

### Frontend (ESLint + Prettier)

**ESLint**: Flat config (`eslint.config.js`)
- TypeScript ESLint parser
- Svelte plugin
- Prettier 연동

**Prettier** (`.prettierrc`):
```
- 탭 사용 (width: 4)
- 싱글 쿼트
- 세미콜론 없음
- trailing comma 없음
- print width: 100
- Svelte plugin
- Import 정렬 (@trivago/prettier-plugin-sort-imports)
```
