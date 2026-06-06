# 테스트 전략

모노레포(`frontend` + `backend`)의 테스트 계층과 그 책임 경계를 정의한다.
실행 명령은 [domain/build-test.md](domain/build-test.md) 또는 루트 `make` 를 참고한다.

## 한눈에 보기

| 계층 | 도구 | 위치 | 백엔드 | 책임 |
|------|------|------|--------|------|
| 백엔드 단위/통합 | pytest | `backend/tests` | 실제(SQLite) | **API 계약의 진실 소스** |
| 프론트 유닛 | Vitest | `frontend/tests/unit` | 없음 | 순수 로직 / 컴포넌트 단위 |
| 프론트 E2E | Playwright | `frontend/tests` | **mock** | 유저 플로우 / UI 상태 전이 |

핵심 원칙: **E2E 는 프론트엔드에 두고 백엔드를 mock 한다.** 실제 백엔드를 띄우지
않으므로 빠르고 결정적이며, CI 에서 프론트 job 이 백엔드에 의존하지 않는다.

## 계층별 책임

### 1. 백엔드 (pytest) — 계약의 진실 소스
- 실제 응답 shape, 상태 코드, 인증/권한 규칙을 검증한다.
- E2E 의 mock 은 "백엔드가 이렇게 응답한다"는 **가정**이다. 그 가정이 실제와
  같다는 보증은 오직 여기서 나온다.
- 따라서 응답 계약이 바뀌면 반드시 여기 테스트가 먼저 바뀌어야 한다.

### 2. 프론트 유닛 (Vitest)
- 네트워크/렌더링에 의존하지 않는 순수 로직(파서, 포매터, 스토어 등)과
  좁은 범위의 컴포넌트 단위를 검증한다.
- 백엔드 호출이 필요하면 그 테스트는 유닛이 아니라 E2E 계층으로 올린다.

### 3. 프론트 E2E (Playwright) — 백엔드 mock
- 실제 사용자 플로우(로그인, 세션 진입, 권한 분기 등)와 UI 상태 전이를 검증한다.
- 백엔드 응답은 `page.route('**/localhost:8000/**')` 로 가로채 mock 한다
  ([tests/helpers/api-mocks.ts](../frontend/tests/helpers/api-mocks.ts)).
- 이 구조가 동작하는 이유: **데이터 페칭이 전부 클라이언트사이드**다. SvelteKit
  `load`(예: `session/[id]/+page.ts`)는 라우팅 파라미터만 계산하고, 실제 API
  호출은 브라우저에서 일어난다. 그래서 `page.route` 가 모든 백엔드 호출을
  가로챌 수 있다. (서버사이드 `load` 에서 fetch 하면 가로채지 못하므로, 새
  데이터 로딩을 추가할 때 이 전제를 깨지 않도록 주의한다.)

## mock 의 정확성을 지키는 법 — 계약 스냅샷

mock 기반 E2E 의 유일한 맹점은 **"mock 이 실제 백엔드와 다를 수 있다"** 는 것이다.
이를 구조적으로 막기 위해 OpenAPI 계약을 스냅샷으로 고정한다.

```
backend 코드 ──(export)──> backend/openapi.json ──(openapi-ts)──> 프론트 API client
                              (단일 진실 소스)                        types.gen.ts 등
                                                                         │
                                          mock factory 가 이 타입을 사용 ─┘
```

- 백엔드는 `backend/openapi.json` 을 커밋된 스냅샷으로 export 한다
  (`make export-spec`). 프론트 client 는 라이브 URL 이 아니라 이 파일에서 생성된다.
- mock factory([api-mocks.ts](../frontend/tests/helpers/api-mocks.ts))는 생성된
  타입(`types.gen.ts`)을 사용하므로, 백엔드 응답 shape 가 바뀌면 타입이 바뀌고
  mock 도 컴파일 단계에서 깨진다 → silent drift 차단.
- CI 가드:
  - 백엔드: `export_openapi.py --check` 로 **코드 ↔ 스냅샷** 동기화 검증
  - 프론트: client 재생성 후 `git diff --exit-code` 로 **스냅샷 ↔ client** 검증

### 계약을 바꿀 때 워크플로우
```bash
# 백엔드 응답/스키마를 수정한 뒤
make gen-client      # 스냅샷 재생성 + 프론트 client 재생성
make check-spec      # drift 없는지 검증 (CI 와 동일)
# backend/openapi.json + frontend/src/lib/api/client 를 함께 커밋
```
빠뜨리면 CI 가 빨갛게 된다.

## 실행 (루트 통합)

| 명령 | 내용 |
|------|------|
| `make test` | 백엔드 + 프론트 전체 |
| `make test-be` | 백엔드 pytest |
| `make test-e2e` | 프론트 E2E (백엔드 mock) |
| `make test-unit` | 프론트 Vitest 유닛 |
| `make check-spec` | 계약 drift 검증 |

개별 도구 직접 실행은 [domain/build-test.md](domain/build-test.md) 참고.
