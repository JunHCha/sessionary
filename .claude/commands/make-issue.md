---
description: 이슈 생성 또는 기존 이슈에 계획서 보강
argument-hint: <issue-number | 자연어 요구사항>
---

# Issue Maker

입력: $ARGUMENTS

## Phase 0: 분기 판단

1. 입력이 숫자인지 확인
   - 숫자 아님 → **분기 A** (새 이슈 생성)
   - 숫자임 → **분기 B** (기존 이슈 보강)

---

## 분기 A: 새 이슈 생성

자연어 요구사항으로 새 GitHub 이슈를 생성한다.

### A.1 맥락 수집

1. 입력에서 도메인 키워드 추출
2. `/spec-loader` 매핑 테이블 참고하여 관련 문서 로드:

| 키워드 | 문서 |
|--------|------|
| lecture, 강의, 티켓 | `docs/spec/domain/lecture.md` |
| session, 세션 | `docs/spec/domain/session.md` |
| subscription, 구독, plan | `docs/spec/domain/subscription.md` |
| folder, 재생목록 | `docs/spec/domain/folder.md` |
| video, streaming, cloudflare | `docs/spec/infrastructure/video-streaming.md` |
| player, 플레이어, hls | `docs/spec/frontend/video-player.md` |
| design, token, 색상 | `docs/spec/design/design-tokens.md` |

3. Grep/Glob으로 영향받는 파일 탐색

### A.2 이슈 분석

다음 항목을 분석한다:
1. 요구사항이 해결하려는 핵심 문제
2. 현재 코드베이스 상태
3. 필요한 변경 범위
4. 잠재적 리스크

### A.3 사용자 확인

AskUserQuestion으로 의사결정이 필요한 사항 질문 (최대 6개):

```text
예시 질문:
- "이 기능은 A 방식과 B 방식 중 어느 것으로 구현할까요?"
- "에러 처리는 어느 수준까지 필요한가요?"
- "기존 API를 변경해도 될까요, 새 API를 추가할까요?"
```

### A.4 이슈 생성

계획서 템플릿(하단 참조) 형식으로 body 작성 후:

```bash
gh issue create --title "{제목}" --body "{계획서 내용}"
```

### A.5 Project에 추가

생성된 이슈를 GitHub Project에 추가:

```bash
gh project item-add <PROJECT_NUMBER> --owner @me --url <이슈URL>
```

생성된 이슈 번호를 사용자에게 알린다.

---

## 분기 B: 기존 이슈 보강

제목만 있는 이슈에 계획서를 추가한다.

### B.1 이슈 정보 수집

```bash
gh issue view $ARGUMENTS --json title,body,labels
```

### B.2 맥락 수집

이슈 제목에서 키워드를 추출하여 분기 A.1과 동일하게 진행

### B.3 이슈 분석

분기 A.2와 동일

### B.4 사용자 확인

분기 A.3과 동일

### B.5 이슈 업데이트

계획서 템플릿 형식으로 body 작성 후:

```bash
gh issue edit $ARGUMENTS --body "{계획서 내용}"
```

### B.6 Project에 추가

이슈가 Project에 없으면 추가:

```bash
gh project item-add <PROJECT_NUMBER> --owner @me --url <이슈URL>
```

---

## 계획서 템플릿

```markdown
## 1. 문제 정의

### 1.1 현재 상황
{현재 시스템의 상태 또는 문제 상황 설명}

### 1.2 해결하고자 하는 문제
{이슈가 해결하려는 핵심 문제}

### 1.3 기대 결과
{이슈가 완료되면 얻을 수 있는 결과}

## 2. 해결 방안

### 2.1 접근 방식
{선택한 해결 방식과 그 이유}

### 2.2 구현 세부사항
{구체적인 구현 방법}

### 2.3 의사결정 사항
| 항목 | 결정 내용 | 이유 |
|------|----------|------|
| {decision_1} | {choice_1} | {reason_1} |

## 3. 영향받는 파일

### 3.1 수정 대상
| 파일 경로 | 변경 내용 |
|----------|----------|
| {file_path_1} | {change_description_1} |

### 3.2 신규 생성
| 파일 경로 | 용도 |
|----------|------|
| {new_file_1} | {purpose_1} |

## 4. 테스트 전략

### 4.1 테스트 케이스
| 케이스 | 타입 | 설명 |
|--------|------|------|
| {test_1} | approval | {description_1} |
| {test_2} | edge_case | {description_2} |

## 5. 작업 체크리스트

- [ ] {task_1}
- [ ] {task_2}
- [ ] {task_3}

## 6. 관련 문서

- spec 문서: {참조한 spec 문서 목록}
```

---

## 출력

완료시 진행 상황 요약:
- 생성/수정된 이슈 번호
- 다음 단계 안내: `/resolve-issue {이슈번호}`로 개발 진행
