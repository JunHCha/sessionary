---
created: 2025-01-03
updated: 2026-01-24T12:00
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

## Session Detail 연동 기능

VideoPlayer는 Session Detail 페이지에서 다른 컴포넌트들과 연동됩니다.

### timeupdate 이벤트 발행

- 비디오 재생 시 `timeupdate` 이벤트를 발행하여 현재 재생 시간을 다른 컴포넌트에 전달
- **연동 대상**:
  - SubtitlePanel: 현재 시간에 맞는 자막 하이라이트 및 자동 스크롤
  - TabSheet: alphaTab tickPosition API를 통한 악보 커서 동기화

### currentTime 전달 구조

```
VideoPlayer
    │
    ├─ timeupdate event ─→ SubtitlePanel (자막 연동)
    │
    └─ timeupdate event ─→ TabSheet (악보 연동, tickPosition API)
```

- 부모 컴포넌트(Session Detail 페이지)에서 `currentTime` 상태를 관리
- VideoPlayer에서 `on:timeupdate` 이벤트로 시간 정보 전달
- 각 연동 컴포넌트는 props로 `currentTime`을 받아 해당 위치 표시

## 추가 컴포넌트 계획

Session Detail Type 1 (Full Tutorial) 레이아웃에 필요한 추가 컴포넌트입니다.

### SubtitlePanel

- **파일**: `frontend/src/lib/features/session/components/SubtitlePanel.svelte` (새 파일)
- **기능**: 비디오 연동 자막 패널
- 주요 기능:
  - 현재 재생 시간에 맞는 자막 하이라이트
  - 자동 스크롤 (현재 자막이 항상 보이도록)
  - 자막 클릭 시 해당 시간으로 비디오 이동 (seek)

### TabSheet

- **파일**: `frontend/src/lib/features/session/components/TabSheet.svelte` (새 파일)
- **기능**: alphaTab 기반 Guitar Pro 파일 렌더링
- 주요 기능:
  - Guitar Pro 파일 (GP 3-7) 렌더링
  - 비디오와 동기화된 재생 커서 표시
  - 내장 MIDI 신디사이저 지원

### PlayingGuide

- **파일**: `frontend/src/lib/features/session/components/PlayingGuide.svelte` (새 파일)
- **기능**: 정적 연주 가이드 표시
- 주요 기능:
  - 세로 스크롤 가능한 가이드 텍스트/이미지
  - **비디오 연동 없음** (정적 콘텐츠)

## alphaTab 연동

TabSheet 컴포넌트에서 사용할 alphaTab 라이브러리 연동 계획입니다.

### 라이브러리 정보

- **라이브러리**: [alphaTab](https://alphatab.net/)
- **라이선스**: MIT
- **지원 포맷**: Guitar Pro 3-7 (.gp3, .gp4, .gp5, .gpx, .gp)

### Guitar Pro 파일 업로드 방식

- 강사가 세션 생성 시 Guitar Pro 파일을 업로드
- 업로드된 파일은 MinIO/Cloudflare에 저장
- 프론트엔드에서 파일 URL을 받아 alphaTab으로 렌더링

### 비디오-악보 동기화

- **tickPosition API**: alphaTab의 `tickPosition` 속성을 사용하여 악보 재생 위치 제어
- **동기화 흐름**:
  1. VideoPlayer에서 `timeupdate` 이벤트 발생
  2. 비디오 currentTime을 tick 값으로 변환
  3. alphaTab의 `tickPosition` 설정으로 커서 이동
- **시간-틱 매핑**: 세션 메타데이터에 동기화 오프셋 정보 저장
