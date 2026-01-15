---
created: 2025-12-21T01:18
updated: 2026-01-15T23:30
---

# Sessionary 프로젝트 기획

기독교 찬양 밴드 세션(특히 기타 세션) 강의를 제공하는 웹 플랫폼입니다.

## 비즈니스 모델

4가지 구독 플랜 제공:

- **Ticket**: 기본 플랜, 주 3개 Lecture 수강
- **Experimental**: Personal 체험판 (2주)
- **Personal**: 무제한 이용 (월 단위 결제)
- **Group**: 다인 할인 적용

## 문서 구조

```
.claude/spec/
├── README.md                    # 프로젝트 개요 (이 파일)
├── domain/                      # 도메인 용어 및 비즈니스 로직
│   ├── lecture.md              # Lecture 용어 + 티켓 시스템
│   ├── session.md              # Session 타입
│   ├── subscription.md         # 구독 플랜
│   └── folder.md               # 커스텀 재생목록
├── infrastructure/              # 인프라 설정
│   └── video-streaming.md      # 비디오 스트리밍 (Cloudflare/MinIO)
├── frontend/                    # 프론트엔드 구현
│   └── video-player.md         # 비디오 플레이어 구현 계획
└── design/                      # 디자인 시스템
    └── design-tokens.md        # 디자인 토큰
```

> **Note**: API 명세는 backend 코드(`/docs` 엔드포인트)가 Single Source of Truth입니다.

## 문서 카테고리

### Domain (도메인)

도메인 개념과 비즈니스 로직을 설명합니다.

| 문서                           | 설명                            |
| ------------------------------ | ------------------------------- |
| [domain/lecture.md]            | Lecture 용어 + 티켓 시스템      |
| [domain/session.md]            | Session 타입 정의               |
| [domain/subscription.md]       | 구독 플랜 종류 및 규칙          |
| [domain/folder.md]             | 커스텀 재생목록 (Folder) 개념   |

### Infrastructure (인프라)

인프라 구성 및 설정 정보입니다.

| 문서                                   | 설명                                 |
| -------------------------------------- | ------------------------------------ |
| [infrastructure/video-streaming.md]    | 비디오 스트리밍 (Cloudflare/MinIO)   |

### Frontend (프론트엔드)

프론트엔드 구현 계획 및 가이드입니다.

| 문서                           | 설명                            |
| ------------------------------ | ------------------------------- |
| [frontend/video-player.md]     | 비디오 플레이어 구현 계획       |

### Design (디자인)

디자인 시스템 및 토큰 정보입니다.

| 문서                           | 설명                            |
| ------------------------------ | ------------------------------- |
| [design/design-tokens.md]      | 색상, 타이포그래피 등 디자인 토큰 |

[domain/lecture.md]: ./domain/lecture.md
[domain/session.md]: ./domain/session.md
[domain/subscription.md]: ./domain/subscription.md
[domain/folder.md]: ./domain/folder.md
[infrastructure/video-streaming.md]: ./infrastructure/video-streaming.md
[frontend/video-player.md]: ./frontend/video-player.md
[design/design-tokens.md]: ./design/design-tokens.md
