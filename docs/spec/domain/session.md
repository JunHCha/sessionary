---
created: 2025-12-21T01:24
updated: 2026-01-24T12:00
---

# Session

Lecture를 구성하는 개별 강의 단위입니다.

## Session 타입

각 Session은 5가지 타입 중 하나로 분류됩니다:

| 타입      | 라벨    | 색상           | 설명                                  |
| --------- | ------- | -------------- | ------------------------------------- |
| 연주 강의 | `PLAY`  | 초록 `#22C55E` | 연주 영상과 해당 마디의 TAB 악보 제공 |
| 곡 해석   | `TALK`  | 파랑 `#3B82F6` | 연주 영상 및 나레이션 (영상 중심)     |
| 리허설    | `JAM`   | 노랑 `#F59E0B` | 백업 트랙에 맞춰 연주 연습 환경 제공  |
| 기본기    | `BASIC` | 보라 `#8B5CF6` | 테크닉 기초 강의 (연주 강의와 유사)   |
| 악보      | `SHEET` | 핑크 `#EC4899` | TAB/악보 이미지 모음                  |

## Session Detail 레이아웃

Session Detail 페이지는 3가지 레이아웃 타입으로 구성됩니다:

| 레이아웃 | 구성 요소 | 적용 세션 타입 |
|----------|----------|---------------|
| Type 1 (Full Tutorial) | 비디오 + 자막 + 탭 악보 + 가이드 | PLAY, BASIC |
| Type 2 (Video Focus) | 비디오 + 자막 패널 | TALK |
| Type 3 (Practice) | 오디오 플레이어 + 탭 악보 | JAM, SHEET |

### Type 1 레이아웃 상세

- 상단: 비디오 + 자막 패널 (나란히 배치)
- 중단: 탭 악보 (alphaTab, 전체 너비)
- 하단: 연주 가이드 (스크롤 가능)
- 연동: 비디오 → 자막/탭 동기화

## Session Detail API

### 엔드포인트

```http
GET /session/{session_id}
```

- 인증 필수
- 티켓/구독 검증 후 접근 허용

### 데이터 구조

#### subtitles (자막)

```json
[
  {"timestamp_ms": 0, "text": "이 파트에서는..."},
  {"timestamp_ms": 12000, "text": "Am 코드에서 시작해서..."}
]
```

#### playing_guide (연주 가이드)

```json
[
  {
    "step": 1,
    "title": "코드 포지션 잡기",
    "description": "Am 코드 형태로 손가락을 배치...",
    "start_time": "0:00",
    "end_time": "0:28",
    "tip": "처음에는 코드를 천천히 잡고..."
  }
]
```

### 응답 예시

```json
{
  "id": 1,
  "title": "아르페지오 인트로 마스터하기",
  "session_type": "PLAY",
  "session_type_label": "연주 강의",
  "lecture_ordering": 2,
  "length_sec": 168,
  "lecture": {
    "id": 1,
    "title": "Stairway to Heaven - Led Zeppelin",
    "total_sessions": 10
  },
  "video": {
    "url": "https://...",
    "type": "hls",
    "expires_at": "2027-01-01T12:00:00Z"
  },
  "sheetmusic_url": "https://.../stairway.gp",
  "sync_offset": 0,
  "subtitles": [],
  "playing_guide": [],
  "navigation": {
    "prev_session_id": null,
    "next_session_id": 2
  }
}
```
