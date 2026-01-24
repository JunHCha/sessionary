---
description: 계획서가 있는 이슈를 TDD 방식으로 해결 (worktree 기반 병렬 작업)
argument-hint: <issue-number>
---

# Issue Resolver (Worktree)

입력: $ARGUMENTS

## Phase 0: 사전 확인

1. 이슈 조회:
   ```bash
   gh issue view $ARGUMENTS --json title,body,state
   ```

2. 계획서 존재 확인:
   - body에 `## 요구사항` 또는 `## 해결 방안` 섹션이 있는지 확인
   - 없으면 `/make-issue $ARGUMENTS`로 계획서 작성 안내 후 중단

---

## Phase 1: 계획서 파싱

이슈 body에서 다음 정보 추출:
- 작업 목록 (`## 작업 목록`)
- 영향 범위 (`## 영향 범위`)

---

## Phase 2: 작업 환경 준비 (Worktree)

1. 브랜치명 생성:
   ```bash
   ISSUE_TITLE=$(gh issue view $ARGUMENTS --json title -q '.title')
   BRANCH_SUFFIX=$(echo "$ISSUE_TITLE" | sed 's/[^가-힣a-zA-Z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | cut -c1-50)
   BRANCH_NAME="${ARGUMENTS}-${BRANCH_SUFFIX}"
   ```

2. Worktree 생성:
   ```bash
   WORKTREE_PATH="../worktrees/${BRANCH_NAME}"
   git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
   ```

3. 작업 디렉토리 이동 및 의존성 설치:
   ```bash
   cd "$WORKTREE_PATH"
   pnpm install
   ```

4. 사용자에게 worktree 경로 안내

---

## Phase 3: TDD 개발

`tdd-worker` sub-agent를 Task tool로 호출하여 개발 수행:

- **worktree 경로를 명시적으로 전달**
- 계획서 기반 RED-GREEN-REFACTOR 사이클 반복
- 커밋당 변경사항 100줄 이하 유지
- edge case 위주 테스트, approval case 1개 이상

---

## Phase 4: 브랜치 분리 처리

tdd-worker가 누적 800줄 초과를 보고하면:

1. `/manage-project draft-pr` 호출하여 현재 작업 PR 생성
2. `/manage-project link-pr` 호출하여 이슈에 PR 연결
3. 사용자에게 알림: "코드 리뷰 후 계속 진행하거나 `/pr-review-resolver`로 리뷰 처리"
4. 파이프라인 일시 중단

---

## Phase 5: 작업 완료

tdd-worker가 작업 완료를 보고하면:

1. `/manage-project draft-pr` 호출하여 Draft PR 생성
2. `/manage-project link-pr` 호출하여 이슈에 PR 연결
3. 사용자에게 self code review 안내

4. **Worktree 정리 안내**:
   ```bash
   # 메인 레포로 돌아간 후 실행
   cd /path/to/sessionary
   git worktree remove "../worktrees/${BRANCH_NAME}"
   ```
   - PR 머지 전까지는 worktree 유지 권장
   - 머지 후 정리 명령어 제공

---

## 출력

각 Phase 완료시 진행 상황 요약:
- 완료된 작업
- 생성된 커밋/PR
- Worktree 경로 및 상태
- 다음 단계 안내
