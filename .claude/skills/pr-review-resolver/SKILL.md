---
name: pr-review-resolver
description: PR 코드 리뷰 코멘트를 체계적으로 해결하는 skill. 사용자가 (1) PR 리뷰 코멘트 해결을 요청하거나, (2) 코드 리뷰 피드백을 반영하려고 하거나, (3) "리뷰 코멘트", "PR 코멘트", "코드 리뷰" 관련 수정을 언급할 때 사용. 1 코멘트 → 1 작업 → 1 테스트 → 1 커밋의 원칙으로 진행하며 진행 상황을 YAML로 추적.
---

# PR Review Resolver

PR에 달린 코드 리뷰 코멘트를 체계적으로 해결한다.

## Workflow

### 0. GitHub 상태 조회 (GraphQL)

먼저 GraphQL API로 review thread의 상태만 가볍게 조회한다 (context 비용 절감):

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          comments(first: 1) {
            nodes { databaseId }
          }
        }
      }
    }
  }
}' -f owner=:owner -f repo=:repo -F pr=$(gh pr view --json number -q .number)
```

**GitHub 코멘트 상태 필드**:
- `isResolved`: GitHub UI에서 "Resolve conversation" 버튼으로 해결됨
- `isOutdated`: 해당 코드 라인이 변경되어 outdated 됨

### 1. Progress 파일 재사용 판단

`.pr-review-progress.yaml` 파일이 존재하면:

1. GraphQL로 미해결 코멘트 ID 목록 조회 (`isResolved: false` AND `isOutdated: false`)
2. progress 파일의 pending 코멘트 ID 목록과 비교
3. **일치**: 기존 progress 파일 재사용, pending 코멘트부터 작업 계속
4. **불일치**: progress 파일 재작성

불일치 판단 기준:
- progress의 pending 코멘트가 GraphQL에서 resolved/outdated로 변경됨
- GraphQL에 새로운 미해결 코멘트가 추가됨

### 2. 코멘트 수집 (필요시)

progress 파일이 없거나 상태 불일치 시, **미해결 코멘트만** 수집한다.

GraphQL API를 사용하여 `isResolved: false` AND `isOutdated: false`인 코멘트만 가져온다:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          comments(first: 1) {
            nodes {
              databaseId
              body
              author { login }
            }
          }
        }
      }
    }
  }
}' -f owner=:owner -f repo=:repo -F pr=$(gh pr view --json number -q .number) \
  --jq '.data.repository.pullRequest.reviewThreads.nodes
    | map(select(.isResolved == false and .isOutdated == false))
    | .[] | {
        thread_id: .id,
        github_comment_id: .comments.nodes[0].databaseId,
        path: .path,
        line: .line,
        body: .comments.nodes[0].body,
        author: .comments.nodes[0].author.login
      }'
```

**제외 대상**:
- `isResolved: true` - GitHub에서 이미 해결됨
- `isOutdated: true` - 코드 변경으로 더 이상 유효하지 않음

### 3. 진행 상황 추적 파일 생성

`.pr-review-progress.yaml` 파일을 생성하여 진행 상황을 추적한다.

**참고**: 수집 단계에서 resolved/outdated 코멘트는 이미 제외되었으므로, progress 파일에는 미해결 코멘트만 포함된다.

```yaml
pr_number: 123
total_comments: 2
resolved: 0
comments:
  - id: 1
    thread_id: "PRT_xxx"           # GraphQL thread ID (상태 조회용)
    github_comment_id: 2686928751  # REST API comment ID (답글 작성용)
    file: backend/app/lesson/view.py
    line: 47
    summary: "video_url 유효성 검사 누락"
    status: pending                # pending | in_progress | resolved | skipped
    commit_sha: null
    skip_reason: null

  - id: 2
    thread_id: "PRT_yyy"
    github_comment_id: 2686928752
    file: backend/app/ticket/repository.py
    line: 58
    summary: "timezone-aware datetime 비교 불일치"
    status: pending
    commit_sha: null
    skip_reason: null
```

### 4. 반복 실행 (1 코멘트 → 1 작업 → 1 테스트 → 1 커밋)

각 코멘트에 대해 다음 순서로 진행:

1. **작업 시작**: 해당 코멘트의 status를 `in_progress`로 변경
2. **코드 수정**: 코멘트에서 제안한 수정 사항 반영
3. **테스트 실행**: 관련 테스트 실행하여 수정 검증
4. **커밋 생성**: 해당 코멘트에 대한 단일 커밋 생성
5. **상태 업데이트**: status를 `resolved`로 변경, commit_sha 기록

#### 커밋 메시지 형식

```text
fix: <간단한 설명>

<상세 설명 (선택)>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### 5. 스킵 기준

다음 경우 코멘트를 `skipped`로 표시:
- 구현에 필요한 외부 의존성이 있지만 현재 사용할 수 없는 경우 (예: API 키, 설정 값)
- 코멘트가 "향후 구현" 또는 "추후 개선"을 언급한 경우
- 현재 PR 범위를 벗어나는 대규모 리팩토링을 요구하는 경우

스킵 시 사유를 `skip_reason` 필드에 기록한다.

**참고**: `isResolved`, `isOutdated` 코멘트는 수집 단계에서 이미 제외됨

### 6. 완료 및 GitHub 코멘트 작성

모든 코멘트가 `resolved` 또는 `skipped` 상태가 되면:

1. 전체 테스트 실행으로 최종 검증
2. **GitHub PR에 결과 코멘트 작성**: `scripts/post_comments.py` 실행

```bash
python3 .claude/skills/pr-review-resolver/scripts/post_comments.py
```

스크립트는 각 코멘트에 대해:
- `resolved`: "Resolved in commit `abc1234`" 형식으로 답글 작성
- `skipped`: "Skipped: <사유>" 형식으로 답글 작성

3. `.pr-review-progress.yaml` 파일 삭제

## Scripts

### post_comments.py

`.pr-review-progress.yaml`을 읽고 GitHub PR 코멘트에 결과를 답글로 작성한다.

```bash
# 실행 (저장소 루트에서)
python3 .claude/skills/pr-review-resolver/scripts/post_comments.py

# 테스트 (실제 코멘트 작성 없이 출력만)
python3 .claude/skills/pr-review-resolver/scripts/post_comments.py --dry-run
```

**요구사항**: `pyyaml` 패키지, `gh` CLI

## 주의사항

- 각 커밋은 단일 코멘트에 대한 수정만 포함해야 한다
- 관련성 높은 코멘트들은 함께 처리할 수 있으나, 명시적으로 기록해야 한다
- 테스트 실패 시 커밋하지 않고 문제를 먼저 해결한다
- `github_comment_id`는 반드시 GitHub API에서 가져온 실제 ID를 사용해야 한다
- 진행 상황 파일은 작업 완료 후 삭제하여 저장소를 깨끗하게 유지한다
