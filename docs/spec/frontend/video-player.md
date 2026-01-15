---
created: 2025-01-03
updated: 2026-01-15T23:30
---

# Frontend 비디오 플레이어 구현 계획

동영상 강의 스트리밍 백엔드 구현 후 진행할 프론트엔드 작업입니다.

## 구현 작업

### 1. 비디오 플레이어 컴포넌트

#### 1.1 VideoPlayer 컴포넌트

- **파일**: `frontend/src/lib/features/lesson/components/VideoPlayer.svelte` (새 파일)
- Cloudflare Stream 플레이어 또는 HTML5 video 태그 사용
- HLS 스트리밍 지원 (`.m3u8`)
- 주요 기능:
  - Signed URL로 비디오 재생
  - 재생 컨트롤 (재생/일시정지, 볼륨, 전체화면)
  - 로딩 상태 표시
  - 에러 처리

#### 1.2 Lesson 상세 페이지 통합

- **파일**: `frontend/src/routes/lecture/[id]/+page.svelte` 또는 관련 컴포넌트
- VideoPlayer 컴포넌트 통합
- 로딩 상태 및 에러 처리
- 접근 권한 없을 때 안내 메시지

#### 1.3 API 클라이언트 확장

- **파일**: `frontend/src/lib/api/client/` (OpenAPI 생성 또는 수동)
- `GET /api/lesson/{id}/video` 엔드포인트 추가
- Signed URL 응답 타입 정의

## 구현 순서

1. **API 클라이언트 확장** (`GET /api/lesson/{id}/video` 엔드포인트)
2. **VideoPlayer 컴포넌트 구현** (기본 재생 기능)
3. **Lesson 상세 페이지 통합** (로딩/에러 처리 포함)
4. **통합 테스트** (로컬 MinIO 환경)

## 비용 최적화 전략

- **Signed URL 캐싱**: Frontend에서 Signed URL을 만료 전까지 캐싱하여 불필요한 API 호출 방지
- **재생 중단 처리**: 사용자가 페이지를 떠나면 스트리밍 중단하여 대역폭 절약

## 기술 스택 고려사항

- **HLS 스트리밍**: Cloudflare Stream은 HLS 형식으로 제공되므로 `hls.js` 라이브러리 고려
- **반응형 디자인**: 모바일/데스크톱 환경 모두 지원
- **접근성**: 키보드 네비게이션 및 스크린 리더 지원
