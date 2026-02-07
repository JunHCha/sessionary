# Architecture

## 디렉토리 구조

```
sessionary/
├── backend/                  # Python FastAPI 백엔드
│   └── app/
│       ├── main.py           # FastAPI 앱 팩토리
│       ├── core/             # 설정, 로깅, 에러, 미들웨어
│       ├── db/               # DB 설정 + Alembic 마이그레이션
│       ├── containers/       # 의존성 주입 컨테이너
│       ├── auth/             # 인증 (fastapi-users, OAuth2, Redis 세션)
│       ├── user/             # 사용자 관리
│       ├── lecture/          # 렉처 도메인
│       ├── lesson/           # 레슨 도메인
│       ├── session/          # 세션 도메인 (5가지 타입)
│       ├── ticket/           # 티켓 시스템
│       ├── subscription/     # 구독 플랜
│       ├── video/            # 비디오 스트리밍 (Cloudflare/MinIO)
│       ├── playlist/         # 플레이리스트
│       └── ping/             # 헬스체크
├── frontend/                 # SvelteKit 프론트엔드
│   └── src/
│       ├── routes/           # 파일 기반 라우팅
│       └── lib/
│           ├── features/     # 기능별 모듈 (auth, lecture, session, ticket)
│           ├── components/   # 공유 UI 컴포넌트
│           ├── api/          # OpenAPI 생성 클라이언트
│           └── utils/        # 유틸리티
├── infra/                    # 인프라 설정
│   ├── dev/                  # Docker Compose (로컬 개발)
│   ├── staging/              # Fly.io 스테이징
│   └── prod/                 # 프로덕션
├── docs/                     # 프로젝트 문서
│   ├── domain/               # 도메인 문서 (이 디렉토리)
│   └── cc/                   # Claude Code 관련 문서
└── .github/workflows/        # CI/CD 파이프라인
```

## 모듈 관계도

```mermaid
graph TB
    subgraph Frontend["Frontend (SvelteKit)"]
        Routes[Routes] --> Features[Feature Modules]
        Features --> ApiClient[OpenAPI Client]
    end

    subgraph Backend["Backend (FastAPI)"]
        Views[Views/Routes] --> Services[Services]
        Services --> Repositories[Repositories]
        Repositories --> DB[(PostgreSQL)]
        Services --> VideoProvider[Video Provider]
        VideoProvider --> MinIO[MinIO<br/>로컬/개발]
        VideoProvider --> Cloudflare[Cloudflare Stream<br/>프로덕션]
    end

    subgraph Infra["Infrastructure"]
        Redis[(Redis)] --> Auth[Auth Sessions]
        Auth --> Views
    end

    ApiClient -->|HTTP/REST| Views
```

## 데이터 흐름

### 요청 처리 흐름

```
Client → SvelteKit SSR/CSR
  → Axios (OpenAPI Client)
    → FastAPI (View)
      → Auth Middleware (Redis 세션 검증)
        → Service (비즈니스 로직)
          → Repository (SQLAlchemy ORM)
            → PostgreSQL
```

### 인증 흐름

```
1. Google OAuth2 → /user/oauth/google/authorize → 리다이렉트 URL 반환
2. Google 콜백 → /user/oauth/google/callback → Redis 세션 생성, 쿠키 설정
3. 이후 요청 → 쿠키의 세션 토큰 → Redis에서 사용자 조회
```

### 세션 접근 흐름

```
1. 렉처 페이지 → 세션 클릭
2. 미인증 → 로그인 모달 → OAuth → 콜백 → 원래 렉처로 복귀
3. 티켓 확인 → /ticket/lecture/{id} → 접근 가능 여부 반환
4. 티켓 사용 → /ticket/lecture/{id} POST → 1주 접근권 부여
5. 세션 상세 → /session/{id} → 비디오 URL + 자막 + 가이드 반환
```

## 비디오 스트리밍 아키텍처

### Cloudflare Stream

| 항목 | 비용 |
|------|------|
| 비디오 저장 | $5 / 1,000분 (월) |
| 비디오 전달(시청) | $1 / 1,000분 |
| 인코딩/업로드/대역폭 | 무료 |

예상 초기 비용: 100개 강의 x 10분 = 1,000분 저장 + 월 10,000분 시청 → **약 $15/월**

### 접근 제어 (Signed URL)

1. 사용자가 Session 접근 요청
2. Backend에서 구독/티켓 상태 확인
3. 유효한 경우 Signed URL 생성 (만료 시간 포함)
4. Frontend에서 Signed URL로 HLS 스트리밍 재생

### 환경별 비디오 제공자

| 환경 | VIDEO_PROVIDER | 스토리지 |
|------|---------------|---------|
| development | local | MinIO (Docker) |
| staging | cloudflare | Cloudflare Stream |
| production | cloudflare | Cloudflare Stream |

### 로컬 MinIO 접속 정보

| 항목 | 값 |
|------|---|
| API | http://localhost:9000 |
| 웹 콘솔 | http://localhost:9001 |
| Access Key | minioadmin |
| Secret Key | minioadmin |
| 버킷 | videos |

### DRM 대안

현재 Signed URL로 제한적 보호. 완벽한 DRM이 필요한 경우 Bunny Stream + DRM 고려 (월 $99 기본 + 라이선스당 비용).

## 프론트엔드 컴포넌트 아키텍처

### Session Detail 컴포넌트 연동

```
VideoPlayer
    │
    ├─ timeupdate event ─→ SubtitlePanel (자막 하이라이트 + 자동 스크롤)
    │
    └─ timeupdate event ─→ TabSheet (alphaTab tickPosition 악보 커서 동기화)
```

- **VideoPlayer**: hls.js + HTML5 video, HLS 스트리밍 재생
- **VideoControls**: 재생/일시정지, 진행률 바, 볼륨, 재생 속도 (0.5x~1.5x), 루프, 전체화면
- **SubtitlePanel**: 현재 시간 기반 자막 하이라이트, 클릭 시 해당 시간으로 seek
- **TabSheet**: alphaTab 기반 Guitar Pro 파일 렌더링, 비디오와 동기화된 커서
- **PlayingGuide**: 정적 연주 가이드 (비디오 연동 없음)

### alphaTab 연동

- Guitar Pro 3-7 (.gp3~.gp) 포맷 지원
- `tickPosition` API로 비디오-악보 동기화
- 동기화 오프셋은 세션 메타데이터(`sync_offset`)에 저장

## 주요 설계 결정

| 결정 | 선택 | 이유 |
|------|------|------|
| 인증 방식 | Redis 세션 쿠키 (JWT 아님) | 서버 측 세션 관리로 즉시 무효화 가능 |
| 비디오 스트리밍 | HLS (Cloudflare Stream) | 적응형 비트레이트, CDN 내장 |
| HLS 라이브러리 | hls.js (~45KB) | 경량, Safari 네이티브 폴백 가능 |
| API 클라이언트 | OpenAPI 코드 생성 | 백엔드 스키마와 타입 자동 동기화 |
| 의존성 주입 | dependency-injector | 테스트 시 Mock 교체 용이 |
| 프론트엔드 반응성 | Svelte 5 Runes | 최신 반응성 모델, 명시적 상태 관리 |
| 악보 렌더링 | alphaTab (MIT) | Guitar Pro 포맷 지원, 비디오 동기화 |
| 배포 | Fly.io | 글로벌 엣지, 간편한 컨테이너 배포 |
