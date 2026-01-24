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

3. 환경 파일 복사:
   ```bash
   # 메인 레포에서 worktree로 env 파일 복사
   MAIN_REPO_PATH="$(pwd)"
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
   else
     echo "No lockfile found. Please run package manager manually."
   fi
   ```

5. 사용자에게 worktree 경로 안내
   - 이후 Phase 3-5는 worktree 디렉토리 내에서 실행됨
   - tdd-worker에게 worktree 절대 경로 전달 필요

---

## Phase 3: TDD 개발

`tdd-worker` sub-agent를 Task tool로 호출하여 개발 수행:

- **worktree 절대 경로를 명시적으로 전달** (예: `$WORKTREE_PATH`)
- 계획서 기반 RED-GREEN-REFACTOR 사이클 반복
- 커밋당 변경사항 100줄 이하 유지
- edge case 위주 테스트, approval case 1개 이상

### Background Task 권한 문제 대응

Background에서 실행 중인 tdd-worker가 권한 요청으로 인해 hang될 경우:

1. **사전 권한 허용**: Task tool 호출 시 `allowed_tools` 파라미터에 필요한 도구 명시
   ```json
   {
     "allowed_tools": ["Bash(yarn *)", "Bash(npm *)", "Bash(pnpm *)", "Bash(pytest *)", "Read", "Edit", "Write"]
   }
   ```

2. **Timeout 설정**: Bash 명령에 timeout 지정 (최대 10분)
   ```json
   {"command": "yarn test", "timeout": 600000}
   ```

3. **진행 상황 모니터링**: `run_in_background: true` 사용 시 주기적으로 TaskOutput 또는 Read로 출력 파일 확인

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

   사용자에게 실제 경로 정보 제공:
   - 메인 레포 경로: `<메인-레포-절대경로>`
   - Worktree 경로: `$WORKTREE_PATH`
   - 브랜치명: `$BRANCH_NAME`

   ```bash
   # worktree 목록 확인
   git worktree list

   # 메인 레포로 이동 후 worktree 제거
   cd <메인-레포-절대경로>
   git worktree remove <worktree-절대경로>
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
