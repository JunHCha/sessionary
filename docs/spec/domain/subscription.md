---
created: 2025-12-21T01:28
updated: 2026-01-15T23:30
---

# Subscription

사용자의 서비스 이용 권한을 정의하는 플랜입니다.

## 규칙

- 모든 사용자는 가입 시 Ticket Plan이 자동 생성됩니다.
- 한 사용자는 하나의 Plan만 가질 수 있습니다.
- Experimental Plan은 직접 활성화하기 전까지 비활성 상태입니다.

## Plan 종류

| Plan         | 이용 범위      | 수명      | Folder | 비고                        |
| ------------ | -------------- | --------- | ------ | --------------------------- |
| Ticket       | 주 3개 Lecture | 무제한    | ❌     | 기본 플랜, 매주 크레딧 충전 |
| Experimental | 무제한         | 2주       | ✅     | Personal의 체험판           |
| Personal     | 무제한         | 결제 기간 | ✅     | 기본 1개월                  |
| Group        | 무제한         | 결제 기간 | ✅     | 다인 할인 적용              |

## Plan 상세

### Ticket Plan

- 기본 플랜 (모든 사용자 자동 적용)
- 주 3개의 Lecture 수강 가능
- 매주 Lecture 크레딧 충전
- Folder 기능 사용 불가

### Experimental Plan

- Personal Plan 체험판
- 무제한 이용 가능
- 2주 후 자동 만료
- 사용자가 직접 활성화해야 시작
- Folder 기능 사용 가능

### Personal Plan

- 무제한 이용 가능
- 결제한 기간만큼 유지 (기본 1개월)
- Folder 기능 사용 가능

### Group Plan

- 무제한 이용 가능
- 여러 명 이용 시 할인 적용
- 결제한 기간만큼 유지
- Folder 기능 사용 가능

## 구현 참고사항

### 결제 연동

- Toss 기준: 클라이언트에서 결제 완료 후 리다이렉트 완료되면 결제 confirm API 호출
- 이미 구독 중인 사용자가 구독 요청 시 실패 처리

### 구독 취소

- 구독 이력은 hard delete하지 않음
- 구독 갱신 시에도 새로운 subscription 데이터 생성
- 갱신 worker가 취소한 사용자를 제외할 수 있어야 함
