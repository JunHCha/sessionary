# Features

## 핵심 기능

### 기능 1: 렉처 시스템
- **설명**: 곡/주제별로 구성된 렉처(강의)를 탐색하고 시청하는 핵심 기능. 각 렉처는 약 10개의 세션으로 구성.
- **관련 파일**: `backend/app/lecture/`, `frontend/src/routes/lecture/[id]/`, `frontend/src/lib/features/lecture/`
- **API 엔드포인트**:
  - `GET /lecture` - 렉처 목록
  - `GET /lecture/{id}` - 렉처 상세 (레슨 목록 포함)

### 기능 2: 세션 (5가지 타입)
- **설명**: 렉처 내 개별 학습 단위. 타입에 따라 다른 레이아웃과 콘텐츠 제공.
- **세션 타입**:
  - **PLAY** (연주): 비디오 + 악보 탭 + 연주 가이드 (Type 1 레이아웃)
  - **TALK** (해설): 비디오 중심 분석 (Type 2 레이아웃)
  - **JAM** (합주): 오디오 + 악보 탭 (Type 3 레이아웃)
  - **BASIC** (기초): 기초 테크닉 (Type 1 레이아웃)
  - **SHEET** (악보): 악보 모음 (Type 3 레이아웃)
- **관련 파일**: `backend/app/session/`, `frontend/src/routes/session/[id]/`, `frontend/src/lib/features/session/`
- **API 엔드포인트**: `GET /session/{id}` - 세션 상세 (비디오 URL, 자막, 가이드 포함)

### 기능 3: 비디오 스트리밍
- **설명**: HLS 적응형 비트레이트 스트리밍. 개발 환경은 MinIO, 프로덕션은 Cloudflare Stream 사용.
- **관련 파일**: `backend/app/video/`, `frontend/src/lib/features/session/components/VideoPlayer.svelte`
- **Provider 전환**: `VIDEO_PROVIDER` 환경변수로 `local`/`cloudflare` 선택

### 기능 4: 인증 (Google OAuth2)
- **설명**: Google OAuth2 기반 로그인. Redis 세션 쿠키로 인증 상태 관리.
- **흐름**: Google 인증 → 콜백 → Redis 세션 생성 → 쿠키 설정 → 인증된 API 호출
- **관련 파일**: `backend/app/auth/`, `frontend/src/routes/oauth-callback/`, `frontend/src/lib/features/auth/`
- **API 엔드포인트**:
  - `GET /user/oauth/google/authorize` - 인증 URL 생성
  - `GET /user/oauth/google/callback` - 콜백 처리
  - `GET /user/me` - 현재 사용자 정보

### 기능 5: 티켓 시스템
- **설명**: 렉처 접근을 위한 티켓 기반 과금 시스템. 티켓 1개로 1주일간 렉처 접근 가능.
- **흐름**: 접근 확인 → 티켓 보유 시 확인 모달 → 사용 → 1주 접근권 부여
- **관련 파일**: `backend/app/ticket/`, `frontend/src/lib/features/ticket/`
- **API 엔드포인트**:
  - `GET /ticket/lecture/{id}` - 접근 상태 확인
  - `POST /ticket/lecture/{id}` - 티켓 사용

### 기능 6: 구독 플랜
- **설명**: 4가지 구독 플랜으로 접근 수준 차별화.
- **플랜**:
  - **ticket**: 주 3개 렉처 기본 (티켓 소모)
  - **experimental**: 무제한 접근
  - **personal**: 무제한 접근
  - **group**: 무제한 접근
- **관련 파일**: `backend/app/subscription/`

## 도메인 개념

### Lecture (렉처)
곡이나 주제를 기반으로 한 강의 묶음. 하나의 렉처에 약 10개의 세션이 포함되며, 아티스트가 제작.

### Session (세션)
렉처 내 개별 학습 단위. 5가지 타입(PLAY, TALK, JAM, BASIC, SHEET)으로 구분되며 각각 고유한 레이아웃을 가짐.

### Ticket (티켓)
렉처 접근 권한 단위. 1티켓 = 1렉처 1주일 접근. 구독 플랜에 따라 주당 제공량이 다름.

### Artist (아티스트)
렉처를 제작하는 사용자. 일반 사용자와 구분되는 `is_artist` 플래그 보유.

## 사용자 플로우

### 신규 사용자 플로우
```
홈 → 렉처 탐색 → 세션 클릭 → 로그인 모달 → Google OAuth
→ 로그인 완료 → 렉처 페이지 복귀 → 티켓 확인 → 세션 시청
```

### 기존 사용자 플로우
```
홈 → 렉처 선택 → 세션 클릭 → 티켓 확인
→ 접근 가능 시 바로 이동 / 불가 시 티켓 부족 모달
→ 세션 상세 → 비디오 시청 + 자막/가이드 활용
→ 이전/다음 세션 네비게이션
```
