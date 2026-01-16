---
description: Backlog 이슈를 분석하고 TDD 방식으로 해결하는 전체 파이프라인 실행
argument-hint: <issue-number>
---

# Resolve Issue Pipeline

이슈 번호: #$ARGUMENTS

## 실행 전 확인

1. `docs/project.md`의 Backlog 섹션에서 해당 이슈가 존재하는지 확인
2. 이슈가 Backlog에 없으면 중단하고 사용자에게 알림

## Phase 1: 기획

`issue-planner` skill을 사용하여:

1. GitHub에서 이슈 정보 조회: `gh issue view $ARGUMENTS --json title,body,labels`
2. 이슈 내용 분석하여 관련 spec 문서 파악
3. `/spec-loader` 매핑 테이블 참고하여 필요한 문서 로드
4. 코드베이스 탐색으로 영향받는 파일 파악
5. 의사결정이 필요한 사항이 있으면 AskUserQuestion으로 질문 (최대 4개)
6. `.plans/$ARGUMENTS-plan.md` 계획서 작성
7. 사용자에게 계획서 승인 요청

**체크포인트**: 사용자가 계획서를 승인해야 다음 Phase로 진행

## Phase 2: 문서 반영

계획서에서 변경된 사항이 있으면:

1. 해당 spec 문서 업데이트 (`docs/spec/` 하위)
2. 변경사항이 `/spec-loader`의 키워드 매핑에 영향을 주면 skill 수정 검토

**체크포인트**: 문서 반영 완료 확인 후 다음 Phase로 진행

## Phase 3: 개발 작업

### 3.1 작업 환경 준비

1. `/project-update` 호출하여 이슈를 "In Progress"로 이동
2. 작업 브랜치 생성: `$ARGUMENTS-{description}`
   ```bash
   # 이슈 제목을 안전하게 브랜치명으로 변환 (한글/특수문자 처리)
   ISSUE_TITLE=$(gh issue view $ARGUMENTS --json title -q '.title')
   BRANCH_SUFFIX=$(echo "$ISSUE_TITLE" | sed 's/[^가-힣a-zA-Z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | cut -c1-50)
   git checkout -b "${ARGUMENTS}-${BRANCH_SUFFIX}"
   ```

### 3.2 TDD 개발

`tdd-worker` sub-agent를 Task tool로 호출하여 개발 수행:

- 계획서 기반 RED-GREEN-REFACTOR 사이클 반복
- 커밋당 변경사항 100줄 이하 유지
- edge case 위주 테스트, approval case 1개 이상

### 3.3 브랜치 분리 처리

tdd-worker가 `[BRANCH_SPLIT_REQUIRED]`를 반환하면:

1. `/project-draft-pr` 호출하여 현재 작업 PR 생성
2. `/project-link-pr` 호출하여 이슈에 PR 연결
3. 사용자에게 알림: "코드 리뷰 후 `/pr-review-resolver`로 리뷰 처리 필요"
4. 파이프라인 일시 중단

### 3.4 작업 완료

tdd-worker가 `[WORK_COMPLETED]`를 반환하면:

1. `/project-draft-pr` 호출하여 Draft PR 생성
2. 사용자에게 self code review 안내
3. "Ready for review" 상태로 변경 전 `/project-link-pr` 실행 권장

## 출력

각 Phase 완료시 진행 상황 요약:
- 완료된 작업
- 생성된 파일/커밋
- 다음 단계 안내
