# Build & Test

## 환경 설정

### 필수 요구사항
- **Python**: >=3.11
- **Node.js**: 20
- **Package Managers**: Poetry (backend), Yarn (frontend)
- **Docker**: 로컬 개발 인프라용 (PostgreSQL, Redis, MinIO)

### 환경 변수

#### Backend (`.env.dev`)
- `APP_ENV` - 환경 (dev/staging/prod/test)
- `SECRET_KEY` - 암호화 키
- `DATABASE_URL` - PostgreSQL 연결 문자열
- `ALLOWED_HOSTS_STR` - CORS 허용 도메인
- `COOKIE_NAME`, `COOKIE_DOMAIN` - 세션 쿠키 설정
- `AUTH_REDIS_URL` - Redis 세션 저장소 URL
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_OAUTH_REDIRECT_URI` - OAuth
- `VIDEO_PROVIDER` - 비디오 제공자 (local/cloudflare)
- `VIDEO_STORAGE_ENDPOINT`, `VIDEO_STORAGE_ACCESS_KEY`, `VIDEO_STORAGE_SECRET_KEY` - S3 호환 Object Storage (로컬: MinIO, Staging: Tigris)

#### Frontend (`.env.development`)
- `PUBLIC_API_BASE_URL` - 백엔드 API 베이스 URL (기본: `http://localhost:8000`)

## 빌드 명령

### Backend

| 명령 | 설명 |
|------|------|
| `poetry install` | 의존성 설치 |
| `alembic upgrade head` | DB 마이그레이션 실행 |
| `docker build -f backend/Dockerfile .` | Docker 이미지 빌드 |

### Frontend

| 명령 | 설명 |
|------|------|
| `yarn install` | 의존성 설치 |
| `yarn build` | 프로덕션 빌드 |
| `yarn generate-client` | OpenAPI 클라이언트 재생성 |
| `docker build -f frontend/Dockerfile .` | Docker 이미지 빌드 |

## 테스트 명령

### Backend

| 명령 | 설명 | 대상 |
|------|------|------|
| `pytest -v tests` | 전체 테스트 | 전체 |
| `pytest -v tests/api/` | API 테스트 | 엔드포인트 |
| `pytest -v tests/session/` | 세션 도메인 테스트 | 세션 로직 |
| `poetry run pytest -v tests` | Poetry 환경에서 실행 | 전체 |

- **DB**: SQLite + aiosqlite (테스트용)
- **설정**: `pyproject.toml` → `[tool.pytest.ini_options]`
- **비동기**: `asyncio_mode = "auto"`

### Frontend

| 명령 | 설명 | 대상 |
|------|------|------|
| `yarn test` | 통합 + 유닛 전체 | 전체 |
| `yarn test:integration` | Playwright E2E 테스트 | 브라우저 (Chromium) |
| `yarn test:unit` | Vitest 유닛 테스트 | 컴포넌트/로직 |
| `npx playwright test tests/routes/session/` | 특정 디렉토리 테스트 | 세션 관련 |
| `npx vitest run` | Vitest 실행 (non-watch) | 유닛 전체 |

- **E2E**: Playwright (Chromium), dev 서버 자동 시작 (port 5173)
- **유닛**: Vitest, 테스트 위치 `tests/unit/**/*.test.ts`
- **타입체크**: `npx svelte-check --tsconfig ./tsconfig.json`

## CI/CD

### GitHub Actions

| 워크플로 | 트리거 | 내용 |
|----------|--------|------|
| `2-test-backend.yml` | PR → `backend/**` | Python 3.11, Poetry, pytest |
| `2-test-frontend.yml` | PR → `frontend/**` | Node 20, Yarn, Playwright + Vitest |
| `deploy-staging-backend.yml` | main 머지 → `backend/**` 또는 `infra/**` | flyctl로 스테이징 배포 후 헬스체크 |
| `deploy-staging-frontend.yml` | main 머지 → `frontend/**` 또는 `infra/**` | flyctl로 스테이징 배포 후 헬스체크 |

### 배포 플랫폼
- **Fly.io**: 스테이징/프로덕션 컨테이너 배포
- **스테이징 앱**: `sessionary-staging-backend`, `sessionary-staging-frontend`
- **배포 스크립트**: `infra/scripts/deploy-staging-backend.sh`, `infra/scripts/deploy-staging-frontend.sh`
- **설정**: `infra/staging/fly-backend.toml`, `infra/staging/fly-frontend.toml`

### 스테이징 시크릿 설정

```bash
# 런북 복사 후 placeholder를 실제 값으로 치환
cp infra/scripts/setup-staging-secrets.example.sh infra/scripts/setup-staging-secrets.sh
# placeholder(<...>) 교체 후 실행
bash infra/scripts/setup-staging-secrets.sh
```

- GitHub Actions 시크릿: `FLY_API_TOKEN_BACKEND`, `FLY_API_TOKEN_FRONTEND`
- 필수 환경변수: `DATABASE_URL`, `AUTH_REDIS_URL`, `SECRET_KEY`, `GOOGLE_CLIENT_ID/SECRET` 등
- 스테이징 Object Storage: Tigris (`VIDEO_STORAGE_ENDPOINT` 등)

## 로컬 개발

### 인프라 시작 (Docker Compose)
```bash
cd infra/dev
docker compose up -d  # PostgreSQL, Redis, MinIO
```

### Backend 개발 서버
```bash
cd backend
poetry install
alembic upgrade head
uvicorn app.main:get_app --reload --host 0.0.0.0 --port 8000
```

### Frontend 개발 서버
```bash
cd frontend
yarn install
yarn dev  # http://localhost:5173
```

### API 클라이언트 재생성
```bash
cd frontend
yarn generate-client  # 백엔드 서버가 실행 중이어야 함
```
