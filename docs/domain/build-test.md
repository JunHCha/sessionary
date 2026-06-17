# Build & Test

## 환경 설정

### 필수 요구사항
- **Python**: >=3.11
- **Node.js**: 20
- **Package Managers**: uv (backend), Yarn (frontend)
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
| `uv sync` | 의존성 설치 |
| `uv run alembic upgrade head` | DB 마이그레이션 실행 |
| `docker build -f backend/Dockerfile .` | Docker 이미지 빌드 |

### Frontend

| 명령 | 설명 |
|------|------|
| `yarn install` | 의존성 설치 |
| `yarn build` | 프로덕션 빌드 |
| `yarn generate-client` | OpenAPI 클라이언트 재생성 (`backend/openapi.json` 스냅샷 기반) |
| `docker build -f frontend/Dockerfile .` | Docker 이미지 빌드 |

## 테스트 명령

> 계층별 책임(유닛 / E2E+mock / 백엔드 계약)과 mock 전략은 [../testing.md](../testing.md) 참고.
> 루트에서 통합 실행하려면 `make test` / `make test-be` / `make test-e2e` 등을 쓴다.

### Backend

| 명령 | 설명 | 대상 |
|------|------|------|
| `uv run pytest -v tests` | 전체 테스트 | 전체 |
| `uv run pytest -v tests/api/` | API 테스트 | 엔드포인트 |
| `uv run pytest -v tests/session/` | 세션 도메인 테스트 | 세션 로직 |

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
| `2-test-backend.yml` | PR → `backend/**` | Python 3.11, uv, OpenAPI 스냅샷 검증, pytest |
| `2-test-frontend.yml` | PR → `frontend/**` 또는 `backend/openapi.json` | Node 20, Yarn, API client 동기화 검증, Playwright + Vitest |
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

### 빠른 시작 (권장): `make devup`
```bash
make devup    # 공유 인프라 기동 + 마이그레이션 + be(:8000)/fe(:5173) 동시 구동
              # Ctrl-C 로 be/fe 둘 다 종료 (인프라는 유지)
make devdown  # 호스트 dev 앱(:8000,:5173)만 종료, 인프라는 유지
```

**전략: 단일 활성 + 공유 인프라.** 인프라(db/redis/minio)는 stateful & worktree 공용이라
`docker compose -p sessionary-dev` 로 한 벌만 띄워 모든 worktree가 공유한다. 앱(be/fe)은
무상태 & 포트 고정(:8000/:5173)이라 활성 worktree 하나에서만 띄운다.
worktree 전환: 현재에서 Ctrl-C → 다른 worktree 에서 `make devup` (인프라 재사용, 앱만 새로).
여러 worktree 의 앱을 *동시에* 띄우려면 포트가 충돌하므로 단일 활성 모델을 쓴다.

아래는 `make devup` 이 내부적으로 수행하는 단계다 (개별 실행/디버깅용).

### 인프라 시작 (Docker Compose)
```bash
make infra-up   # = docker compose -p sessionary-dev -f infra/dev/docker-compose.yml up -d db auth-redis minio minio-init
# 또는 수동:
cd infra/dev && docker compose up -d  # PostgreSQL, Redis, MinIO (+ be/fe 컨테이너까지 전부)
```
> 주의: `infra/dev/docker-compose.yml` 은 backend/frontend 컨테이너(:8000/:3000)도 정의한다.
> 호스트에서 `uv run`/`yarn dev` 로 앱을 띄울 거면 인프라 서비스만 올려야 포트가 안 겹친다
> (`make infra-up` 이 인프라만 선택해서 띄운다).

### Backend 개발 서버
```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:get_app --reload --host 0.0.0.0 --port 8000
```

### Frontend 개발 서버
```bash
cd frontend
yarn install
yarn dev  # http://localhost:5173
```

### API 클라이언트 재생성
프론트 client 는 라이브 백엔드가 아니라 커밋된 스냅파일 `backend/openapi.json`
에서 생성된다. 백엔드 응답 계약을 바꿨다면 스냅샷부터 재생성한다.

```bash
# 루트에서 한 번에 (스냅샷 + client 재생성)
make gen-client
make check-spec   # drift 없는지 검증 (CI 와 동일)

# 개별 실행
cd backend && uv run python dev-scripts/export_openapi.py  # 스냅샷 갱신
cd frontend && yarn generate-client                        # 백엔드 불필요
```

`backend/openapi.json` 과 `frontend/src/lib/api/client` 를 함께 커밋한다.
