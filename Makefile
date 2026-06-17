# Sessionary 모노레포 통합 러너
#
# frontend(yarn) / backend(uv) 가 서로 다른 툴체인을 쓰므로, 디렉토리를 옮겨
# 다니지 않고 루트에서 한 번에 실행하기 위한 얇은 위임 레이어다.
# (소스를 통합하는 것이 아니라 "어디서 무엇을 치는지"만 모은다.)

.PHONY: help install \
        devup devdown infra-up infra-down \
        test test-be test-fe test-unit test-e2e \
        export-spec gen-client check-spec \
        lint format check

# 로컬 인프라 스택. -p 로 프로젝트명을 고정해 어느 worktree 에서 실행하든
# 같은 db/redis/minio(=같은 데이터) 한 벌을 가리키게 한다.
COMPOSE := docker compose -p sessionary-dev -f infra/dev/docker-compose.yml
# stateful 인프라만 (앱 컨테이너 backend/frontend 는 호스트에서 직접 띄운다)
INFRA_SERVICES := db auth-redis minio minio-init
# backend 는 APP_ENV 로 .env.{APP_ENV} 를 고른다. 미설정 시 app_env 기본값(prod)으로
# 떨어져 .env.dev 를 못 읽으므로(설정 누락 에러) 호스트 직접 실행 시 명시해야 한다.
APP_ENV ?= dev
# 호스트 직접 실행은 compose 인프라를 localhost 로 접근한다. .env.dev 의 AUTH_REDIS_URL 은
# 컨테이너 네트워크 호스트명(auth-redis)이라 호스트에서는 DNS 해석이 안 되므로 덮어쓴다.
# (DATABASE_URL 은 .env.dev 가 이미 localhost 라 그대로 쓴다.)
AUTH_REDIS_URL ?= redis://localhost:6379
# devup 의 backend 명령에 공통으로 붙는 호스트-실행용 환경
DEV_BE_ENV := APP_ENV=$(APP_ENV) AUTH_REDIS_URL=$(AUTH_REDIS_URL)

help: ## 사용 가능한 명령 목록
	@echo "Sessionary 통합 명령:"
	@echo "  make install      - fe/be 의존성 설치"
	@echo "  make devup        - 공유 인프라 + be(:8000)/fe(:3000) 개발 서버 동시 구동 (Ctrl-C 로 종료)"
	@echo "  make devdown      - 호스트 dev 앱(:8000,:3000) 종료 (인프라는 유지)"
	@echo "  make infra-up     - 공유 로컬 인프라(db/redis/minio)만 기동"
	@echo "  make infra-down   - 공유 인프라 중지 (볼륨 데이터 보존)"
	@echo "  make test         - 백엔드 + 프론트엔드 전체 테스트"
	@echo "  make test-be      - 백엔드 pytest"
	@echo "  make test-fe      - 프론트엔드 유닛 + e2e"
	@echo "  make test-unit    - 프론트엔드 Vitest 유닛"
	@echo "  make test-e2e     - 프론트엔드 Playwright e2e (백엔드는 mock)"
	@echo "  make export-spec  - 백엔드 OpenAPI 스냅샷(backend/openapi.json) 생성"
	@echo "  make gen-client   - 스냅샷 생성 + 프론트 API client 재생성"
	@echo "  make check-spec   - 계약 drift 검증 (be 코드↔스냅샷, fe 스냅샷↔client)"
	@echo "  make check        - 프론트 타입체크(svelte-check)"
	@echo "  make lint         - fe/be 린트"
	@echo "  make format       - fe/be 포맷"

install: ## fe/be 의존성 설치
	cd backend && uv sync
	cd frontend && yarn install

# --- 로컬 개발 --------------------------------------------------------------
#
# 전략: "단일 활성 + 공유 인프라".
#  - 인프라(db/redis/minio)는 stateful & worktree 공용 → 한 벌만 띄워 공유.
#  - 앱(be/fe)은 무상태 & 포트 고정(:8000/:3000) → 활성 worktree 하나에서만.
#    fe 는 3000: Google OAuth redirect_uri 가 localhost:3000/oauth-callback 기준이라
#    vite 기본값(5173) 대신 3000 으로 강제(--strictPort)해 콜백을 일치시킨다.
# worktree 전환: 현재에서 Ctrl-C(또는 make devdown) → 다른 worktree 에서 make devup.
# 인프라는 재사용되고 앱만 새로 뜬다.

infra-up: ## 공유 로컬 인프라(db/redis/minio) 기동 — worktree 공용, idempotent
	$(COMPOSE) up -d $(INFRA_SERVICES)

infra-down: ## 공유 인프라 중지 (볼륨 데이터는 보존)
	$(COMPOSE) stop $(INFRA_SERVICES)

devup: infra-up ## 공유 인프라 + be/fe 개발 서버 동시 구동 (Ctrl-C 로 둘 다 종료)
	cd backend && $(DEV_BE_ENV) uv run alembic upgrade head
	@echo "▶ backend(:8000) + frontend(:3000) 기동 — Ctrl-C 로 둘 다 종료"
	@trap 'kill 0' INT TERM EXIT; \
	(cd backend && $(DEV_BE_ENV) uv run uvicorn app.main:get_app --reload --host 0.0.0.0 --port 8000) & \
	(cd frontend && yarn dev --port 3000 --strictPort) & \
	wait

devdown: ## 호스트 dev 앱(:8000,:3000) 종료 — 인프라는 유지
	-@pids=$$(lsof -ti tcp:8000); [ -n "$$pids" ] && kill $$pids 2>/dev/null || true
	-@pids=$$(lsof -ti tcp:3000); [ -n "$$pids" ] && kill $$pids 2>/dev/null || true
	@echo "dev 앱 종료. 인프라까지 내리려면 make infra-down."

# --- 테스트 -----------------------------------------------------------------

test: test-be test-fe ## 전체 테스트

test-be: ## 백엔드 pytest
	cd backend && uv run pytest -v tests

test-fe: test-unit test-e2e ## 프론트엔드 전체 (유닛 + e2e)

test-unit: ## 프론트엔드 Vitest 유닛 (non-watch)
	cd frontend && yarn vitest run

test-e2e: ## 프론트엔드 Playwright e2e — 백엔드는 page.route 로 mock
	cd frontend && yarn playwright test

# --- OpenAPI 계약 -----------------------------------------------------------

export-spec: ## 백엔드 OpenAPI 스냅샷 생성
	cd backend && uv run python dev-scripts/export_openapi.py

gen-client: export-spec ## 스냅샷 생성 + 프론트 client 재생성
	cd frontend && yarn generate-client

check-spec: ## 계약 drift 검증 (CI 와 동일)
	cd backend && uv run python dev-scripts/export_openapi.py --check
	cd frontend && yarn generate-client
	@if [ -n "$$(git status --porcelain frontend/src/lib/api/client)" ]; then \
		echo "API client 가 backend/openapi.json 과 다릅니다. 'make gen-client' 후 커밋하세요."; \
		git status --porcelain frontend/src/lib/api/client; \
		exit 1; \
	fi

# --- 품질 -------------------------------------------------------------------

check: ## 프론트 타입체크
	cd frontend && yarn run check

lint: ## fe/be 린트
	cd backend && uv run ruff check .
	cd frontend && yarn lint

format: ## fe/be 포맷
	cd backend && uv run ruff format .
	cd frontend && yarn format
