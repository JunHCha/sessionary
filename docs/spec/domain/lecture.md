---
created: 2025-12-21T01:24
updated: 2026-01-25T12:00
---

# Lecture

하나의 곡에 대한 강의 모음, 또는 특정 주제로 기획된 강의 시리즈입니다.

- 여러 개의 Session으로 구성됨 (약 10개 내외)
- 곡 단위 또는 주제별로 기획

## 접근 권한

| 페이지         | 비로그인         | Ticket Plan        | 무제한 구독 |
| -------------- | ---------------- | ------------------ | ----------- |
| Lecture 목록   | ✅               | ✅                 | ✅          |
| Lecture detail | ✅               | ✅                 | ✅          |
| Session detail | ❌ (로그인 유도) | 티켓 차감 후 접근  | ✅          |
| 비디오 재생    | ❌               | 티켓 사용된 경우만 | ✅          |

## 티켓 시스템

### 티켓 차감 플로우

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant DB

    Note over User,DB: Lecture Detail View (Public)
    User->>Frontend: Lecture 상세 페이지 접근
    Frontend->>Backend: GET /api/lecture/{lecture_id}
    Backend-->>Frontend: Lecture 정보 + Session 목록 (메타정보만)
    Frontend->>User: Lecture 상세 페이지 표시

    Note over User,DB: Session Detail View 진입 시도
    User->>Frontend: Session 클릭 (Session detail view 진입 시도)

    alt 미인증 사용자
        Frontend->>Frontend: sessionStorage에 sessionId 저장
        Frontend->>User: 로그인 모달 표시
        User->>Frontend: 로그인 완료
        Frontend->>Frontend: sessionStorage에서 sessionId 복원
        Frontend->>Frontend: 모달 닫기, 아래 플로우 계속
    end

    Frontend->>Backend: GET /api/ticket/lecture/{lecture_id}
    Note right of Backend: 인증 필요 (401 if 미인증)
    Backend->>DB: TicketUsage 조회 (user_id, lecture_id, 1주 이내)
    Backend->>DB: User 구독 정보 조회

    alt 무제한 구독 (Personal/Group/Experimental)
        Backend-->>Frontend: { accessible: true, reason: "unlimited" }
        Frontend->>Frontend: Session detail view로 이동
    else 이미 티켓 사용됨 (1주 이내)
        Backend-->>Frontend: { accessible: true, reason: "ticket_used", expires_at: ... }
        Frontend->>Frontend: Session detail view로 이동
    else 티켓 미사용 & 티켓 있음
        Backend-->>Frontend: { accessible: false, ticket_count: 3 }
        Frontend->>User: 티켓 차감 확인 모달
        User->>Frontend: 차감 확인
        Frontend->>Backend: POST /api/ticket/lecture/{lecture_id}
        Backend->>DB: TicketUsage 생성 + User.ticket_count 차감
        Backend-->>Frontend: { accessible: true, reason: "ticket_used", expires_at: ... }
        Frontend->>Frontend: Session detail view로 이동
    else 티켓 없음
        Backend-->>Frontend: { accessible: false, ticket_count: 0 }
        Frontend->>User: 티켓 부족 안내 (구독 유도)
    end

    Note over User,DB: Session Detail View 내 비디오 재생
    User->>Frontend: 비디오 재생 요청
    Frontend->>Backend: GET /api/lesson/{lesson_id}/video
    Backend->>DB: TicketUsage 또는 구독 상태 확인
    alt 접근 권한 있음
        Backend->>Backend: VideoProvider.get_video_url()
        Backend-->>Frontend: { url, type, expires_at }
        Frontend->>User: 비디오 재생
    else 접근 권한 없음
        Backend-->>Frontend: 403 Forbidden
    end
```

### 미인증 사용자 처리

미인증 상태에서 Session 클릭 시:

1. **Pending Session 상태 저장**
   - `sessionStorage.setItem('pendingSessionId', sessionId)`로 클릭한 Session ID 저장
   - 로그인 완료 후 티켓 차감 플로우를 자동으로 재개하기 위함

2. **로그인 완료 후 자동 재개**
   - 페이지 마운트 시 (`onMount`) `sessionStorage`에서 `pendingSessionId` 확인
   - 저장된 Session ID가 있으면 티켓 차감 플로우 자동 재개
   - 처리 완료 후 `sessionStorage`에서 해당 값 제거

3. **401 에러 처리**
   - 티켓 접근 확인 API 호출 시 401 에러 발생 시 로그인 모달 표시
   - `sessionStorage`에 현재 Session ID 저장 후 로그인 유도

### 티켓 유효 기간

- 티켓 사용 시 해당 Lecture에 대해 **1주간** 접근 가능
- 1주 후 만료되면 다시 티켓 차감 필요

### 무제한 구독 판단 기준

- `subscription.name` in ["personal", "group", "experimental"]
- `subscription.is_active` = true
- `user.expires_at` > now (만료되지 않음)
