# Source Index

## 핵심 파일 인덱스

### Backend

| 파일 | 역할 | 주요 export |
|------|------|------------|
| `backend/app/main.py` | FastAPI 앱 팩토리 | `create_app()`, `get_app()` |
| `backend/app/core/settings/` | 환경별 설정 | `DevSettings`, `StagingSettings`, `ProdSettings` |
| `backend/app/containers/application.py` | DI 컨테이너 | `ApplicationContainer` |
| `backend/app/auth/backend.py` | 인증 백엔드 | Redis 세션 전략 |
| `backend/app/auth/middleware.py` | 인증 미들웨어 | `AuthSessionMiddleware` |
| `backend/app/lecture/view.py` | 렉처 API 라우트 | 렉처 목록/상세 엔드포인트 |
| `backend/app/lecture/service.py` | 렉처 비즈니스 로직 | `LectureService` |
| `backend/app/lecture/repository.py` | 렉처 DB 접근 | `LectureRepository` |
| `backend/app/session/view.py` | 세션 API 라우트 | 세션 상세 엔드포인트 |
| `backend/app/session/service.py` | 세션 비즈니스 로직 | `SessionService` |
| `backend/app/session/repository.py` | 세션 DB 접근 | `SessionRepository` |
| `backend/app/ticket/view.py` | 티켓 API 라우트 | 접근 확인/사용 엔드포인트 |
| `backend/app/ticket/service.py` | 티켓 비즈니스 로직 | `TicketService` |
| `backend/app/video/service.py` | 비디오 URL 생성 | `VideoService` |
| `backend/app/video/providers/` | 비디오 제공자 | `CloudflareProvider`, `MinioProvider` |
| `backend/app/subscription/models.py` | 구독 모델 | `SubscriptionPlan` enum |

### Frontend

| 파일 | 역할 | 주요 export |
|------|------|------------|
| `frontend/src/routes/+layout.svelte` | 루트 레이아웃 | API 초기화, 인증 상태 |
| `frontend/src/routes/+layout.server.ts` | 서버 로드 | 환경변수 전달 |
| `frontend/src/routes/home/+page.svelte` | 홈 페이지 | 렉처 목록 표시 |
| `frontend/src/routes/lecture/[id]/+page.svelte` | 렉처 상세 | 세션 목록, 티켓 처리 |
| `frontend/src/routes/session/[id]/+page.svelte` | 세션 상세 | 비디오 플레이어, 자막, 가이드 |
| `frontend/src/routes/session/[id]/+page.ts` | 세션 로드 | URL 파라미터 파싱 |
| `frontend/src/routes/oauth-callback/+page.svelte` | OAuth 콜백 | 인증 완료 처리 |
| `frontend/src/lib/api/config.ts` | API 설정 | `initializeApi()`, `waitForApiInit()` |
| `frontend/src/lib/api/client/` | OpenAPI 생성 클라이언트 | 타입, 서비스 함수 |
| `frontend/src/lib/api/session.ts` | 세션 API | `fetchSessionDetail()` |
| `frontend/src/lib/features/auth/stores/` | 인증 스토어 | 로그인 상태 관리 |
| `frontend/src/lib/features/session/services.ts` | 세션 서비스 | `loadSessionDetail()` |
| `frontend/src/lib/features/session/types.ts` | 세션 타입 | `SessionDetailData`, `toSessionDetailData()` |
| `frontend/src/lib/features/session/components/VideoPlayer.svelte` | 비디오 플레이어 | HLS.js 기반 플레이어 |
| `frontend/src/lib/features/lecture/components/SessionList.svelte` | 세션 목록 | 렉처 내 세션 리스트 |
| `frontend/src/lib/features/ticket/` | 티켓 모달 | 확인/부족 모달 |
| `frontend/src/lib/components/Modal.svelte` | 공통 모달 | 재사용 모달 컴포넌트 |

## 엔트리포인트

### Backend
- `backend/app/main.py` → `create_app()` → Uvicorn ASGI 서버
- 모든 라우터는 `create_app()`에서 prefix와 함께 등록

### Frontend
- `frontend/src/app.html` → HTML 템플릿
- `frontend/src/routes/+layout.svelte` → 루트 레이아웃 (API 초기화)
- `frontend/src/routes/+page.svelte` → `/` 접근 시 `/home`으로 리다이렉트

## 공유 유틸리티

### Backend
| 모듈 | 역할 |
|------|------|
| `app/core/errors.py` | 공통 예외 클래스 |
| `app/core/logging.py` | loguru 기반 로깅 설정 |
| `app/core/middlewares.py` | CORS, 인증 미들웨어 |

### Frontend
| 모듈 | 역할 |
|------|------|
| `frontend/src/lib/utils/` | 범용 유틸리티 함수 |
| `frontend/src/lib/components/` | 공유 UI 컴포넌트 (Modal, Layout) |
| `frontend/src/lib/api/config.ts` | API 초기화 및 대기 |
