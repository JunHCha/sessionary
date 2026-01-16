---
name: pr-review-resolver
description: PR 코드 리뷰 코멘트를 체계적으로 해결하는 skill. 사용자가 (1) PR 리뷰 코멘트 해결을 요청하거나, (2) 코드 리뷰 피드백을 반영하려고 하거나, (3) "리뷰 코멘트", "PR 코멘트", "코드 리뷰" 관련 수정을 언급할 때 사용. 1 코멘트 → 1 작업 → 1 테스트 → 1 커밋의 원칙으로 진행하며 진행 상황을 YAML로 추적.
---

# PR Review Resolver

PR에 달린 코드 리뷰 코멘트를 체계적으로 해결한다.

## Workflow

### 1. 코멘트 수집

```bash
gh api repos/:owner/:repo/pulls/$(gh pr view --json number -q .number)/comments \
  --jq '.[] | {id: .id, path: .path, line: .line, body: .body, author: .user.login}'
```

### 2. 진행 상황 추적 파일 생성

`.pr-review-progress.yaml` 파일을 생성하여 진행 상황을 추적한다:

```yaml
pr_number: 123
total_comments: 8
resolved: 0
comments:
  - id: 1
    github_comment_id: 2686928751  # GitHub API에서 가져온 코멘트 ID
    file: backend/app/lesson/view.py
    line: 47
    summary: "video_url 유효성 검사 누락"
    status: pending  # pending | in_progress | resolved | skipped
    commit_sha: null
    skip_reason: null

  - id: 2
    github_comment_id: 2686928752
    file: backend/app/ticket/repository.py
    line: 58
    summary: "timezone-aware datetime 비교 불일치"
    status: pending
    commit_sha: null
    skip_reason: null
```

### 3. 반복 실행 (1 코멘트 → 1 작업 → 1 테스트 → 1 커밋)

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

### 4. 스킵 기준

다음 경우 코멘트를 `skipped`로 표시:
- 구현에 필요한 외부 의존성이 없는 경우 (예: API 키, 설정 값)
- 코멘트가 "향후 구현" 또는 "추후 개선"을 언급한 경우
- 현재 PR 범위를 벗어나는 대규모 리팩토링을 요구하는 경우

스킵 시 사유를 `skip_reason` 필드에 기록한다.

### 5. 완료 및 GitHub 코멘트 작성

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
