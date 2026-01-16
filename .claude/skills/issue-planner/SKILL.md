---
name: issue-planner
description: >
  GitHub 이슈를 분석하고 해결 계획서를 작성하는 skill.
  사용자가 (1) 이슈 기획, 이슈 분석, 계획 수립을 요청하거나,
  (2) backlog 이슈를 해결하려고 하거나,
  (3) 이슈 번호를 언급하며 구현 방법을 물을 때 사용.
  spec-loader와 연동하여 도메인 문서를 참조하고,
  .plans/ 폴더에 계획서를 생성한다.
---

# Issue Planner

GitHub 이슈를 분석하여 구체적인 해결 계획서를 작성한다.

## Workflow

### Step 1: 이슈 정보 수집

```bash
gh issue view {issue_number} --json title,body,labels,assignees
```

### Step 2: 관련 Spec 문서 로드

이슈 내용에서 키워드를 파악하여 `/spec-loader`의 매핑 테이블 참고:

| 키워드 | 문서 |
|--------|------|
| lecture, 강의, 티켓 | `docs/spec/domain/lecture.md` |
| session, 세션 | `docs/spec/domain/session.md` |
| subscription, 구독, plan | `docs/spec/domain/subscription.md` |
| folder, 재생목록 | `docs/spec/domain/folder.md` |
| video, streaming, cloudflare | `docs/spec/infrastructure/video-streaming.md` |
| player, 플레이어, hls | `docs/spec/frontend/video-player.md` |
| design, token, 색상 | `docs/spec/design/design-tokens.md` |

전체 개요 필요시 `docs/spec/README.md` 먼저 읽기.

### Step 3: 이슈 분석

다음 항목을 분석한다:
1. 이슈가 해결하려는 핵심 문제
2. 현재 코드베이스 상태 (Grep, Glob으로 탐색)
3. 필요한 변경 범위
4. 잠재적 리스크

### Step 4: 사용자 확인

AskUserQuestion으로 의사결정이 필요한 사항 질문 (최대 4개):

```
예시 질문:
- "이 기능은 A 방식과 B 방식 중 어느 것으로 구현할까요?"
- "에러 처리는 어느 수준까지 필요한가요?"
- "기존 API를 변경해도 될까요, 새 API를 추가할까요?"
```

### Step 5: 계획서 작성

`.plans/{issue_number}-plan.md` 파일로 저장한다.

계획서 템플릿: `references/plan-template.md`

필수 포함 항목:
- 문제 정의
- 해결 방안 (의사결정 사항 포함)
- 영향받는 파일 목록
- 테스트 전략 (edge case 위주, approval case 1개 이상)
- 작업 체크리스트

### Step 6: 최종 확인

계획서를 사용자에게 보여주고 승인을 받는다.

## 출력 위치

`.plans/` 폴더에 계획서를 저장한다. 폴더가 없으면 생성한다.

```
.plans/
├── 46-plan.md
├── 49-plan.md
└── ...
```

## 연동

- `/spec-loader`: 도메인 spec 문서 참조
- `/project-update`: 이슈 상태 변경 (계획 승인 후)
- `tdd-worker` sub-agent: 실제 개발 작업 (계획 승인 후)
