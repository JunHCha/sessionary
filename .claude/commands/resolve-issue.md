---
description: 계획서가 있는 이슈를 TDD 방식으로 해결
argument-hint: <issue-number>
---

# Issue Resolver (Worktree 기반)

입력: $ARGUMENTS

## Phase 0: 사전 확인

1. **Worktree 환경 확인**:
   ```bash
   # .git이 파일이면 worktree, 디렉토리면 메인 레포
   if [ -f .git ]; then
     echo "WORKTREE"
   else
     echo "MAIN_REPO"
   fi
   ```

   - **결과에 따른 분기**:
     - `WORKTREE`: 현재 worktree 경로를 기록하고 Phase 1로 진행 (새 worktree 생성 불필요)
     - `MAIN_REPO`: Phase 2에서 worktree 생성 진행

2. 이슈 조회:
   ```bash
   gh issue view $ARGUMENTS --json title,body,state
   ```

3. 계획서 존재 확인:
   - body에 `## 요구사항` 또는 `## 해결 방안` 또는 `## 1. 문제 정의` 섹션이 있는지 확인
   - 없으면 `/make-issue $ARGUMENTS`로 계획서 작성 안내 후 중단

---

## Phase 1: 계획서 파싱

이슈 body에서 다음 정보 추출:
- 작업 목록 (`## 작업 목록` 또는 `## 5. 작업 체크리스트`)
- 영향 범위 (`## 영향 범위` 또는 `## 3. 영향받는 파일`)
- 테스트 전략 (`## 4. 테스트 전략`)

---

## Phase 2: 작업 환경 준비

### Case A: 이미 Worktree 내부인 경우

```bash
# 현재 경로를 작업 디렉토리로 사용
WORKTREE_PATH="$(pwd)"
BRANCH_NAME="$(git branch --show-current)"
echo "기존 worktree 사용: $WORKTREE_PATH (브랜치: $BRANCH_NAME)"
```

- Phase 3로 바로 진행

### Case B: 메인 레포인 경우 (Worktree 생성)

1. 브랜치명 생성:
   ```bash
   ISSUE_TITLE=$(gh issue view $ARGUMENTS --json title -q '.title')
   BRANCH_SUFFIX=$(echo "$ISSUE_TITLE" | sed 's/[^가-힣a-zA-Z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | cut -c1-50)
   BRANCH_NAME="${ARGUMENTS}-${BRANCH_SUFFIX}"
   ```

2. Worktree 생성:
   ```bash
   MAIN_REPO_PATH="$(pwd)"
   WORKTREE_PATH="../worktrees/${BRANCH_NAME}"
   git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
   ```

3. 환경 파일 복사:
   ```bash
   [ -f "$MAIN_REPO_PATH/backend/.env.dev" ] && cp "$MAIN_REPO_PATH/backend/.env.dev" "$WORKTREE_PATH/backend/.env.dev"
   [ -f "$MAIN_REPO_PATH/frontend/.env.development" ] && cp "$MAIN_REPO_PATH/frontend/.env.development" "$WORKTREE_PATH/frontend/.env.development"
   ```

4. 작업 디렉토리 이동 및 의존성 설치:
   ```bash
   cd "$WORKTREE_PATH"
   # 패키지 매니저 자동 감지 (lockfile 기반)
   if [ -f "yarn.lock" ]; then
     yarn install
   elif [ -f "pnpm-lock.yaml" ]; then
     pnpm install
   elif [ -f "package-lock.json" ]; then
     npm install
   fi
   ```

5. 사용자에게 worktree 경로 안내

---

## Phase 3: TDD 개발

`tdd-worker` sub-agent를 Task tool로 호출하여 개발 수행.

### tdd-worker 호출 시 필수 파라미터

```json
{
  "subagent_type": "tdd-worker",
  "run_in_background": true,
  "allowed_tools": [
    "Bash(*)",
    "Read",
    "Edit",
    "Write",
    "Grep",
    "Glob"
  ],
  "prompt": "... worktree 절대 경로($WORKTREE_PATH)와 계획서 내용 포함 ..."
}
```

### 개발 원칙

- **worktree 절대 경로를 명시적으로 전달** (예: `$WORKTREE_PATH`)
- 계획서 기반 RED-GREEN-REFACTOR 사이클 반복
- 커밋당 변경사항 100줄 이하 유지
- edge case 위주 테스트, approval case 1개 이상

### 진행 상황 모니터링

`run_in_background: true` 사용 시 주기적으로 TaskOutput 또는 Read로 출력 파일 확인

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

4. **Worktree 정리 안내** (Case B에서 생성한 경우만):

   사용자에게 실제 경로 정보 제공:
   - 메인 레포 경로: `$MAIN_REPO_PATH`
   - Worktree 경로: `$WORKTREE_PATH`
   - 브랜치명: `$BRANCH_NAME`

   ```bash
   # worktree 목록 확인
   git worktree list

   # 메인 레포로 이동 후 worktree 제거
   cd $MAIN_REPO_PATH
   git worktree remove $WORKTREE_PATH
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
