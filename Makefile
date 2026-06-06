# Sessionary 모노레포 통합 러너
#
# frontend(yarn) / backend(uv) 가 서로 다른 툴체인을 쓰므로, 디렉토리를 옮겨
# 다니지 않고 루트에서 한 번에 실행하기 위한 얇은 위임 레이어다.
# (소스를 통합하는 것이 아니라 "어디서 무엇을 치는지"만 모은다.)

.PHONY: help install \
        test test-be test-fe test-unit test-e2e \
        export-spec gen-client check-spec \
        lint format check

help: ## 사용 가능한 명령 목록
	@echo "Sessionary 통합 명령:"
	@echo "  make install      - fe/be 의존성 설치"
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
	cd frontend && yarn generate-client && git diff --exit-code src/lib/api/client \
		|| (echo "API client 가 backend/openapi.json 과 다릅니다. 'make gen-client' 후 커밋하세요." && exit 1)

# --- 품질 -------------------------------------------------------------------

check: ## 프론트 타입체크
	cd frontend && yarn run check

lint: ## fe/be 린트
	cd backend && uv run ruff check .
	cd frontend && yarn lint

format: ## fe/be 포맷
	cd backend && uv run ruff format .
	cd frontend && yarn format
