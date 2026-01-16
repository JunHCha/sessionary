---
description: 이슈 상태 변경 및 project.md 업데이트
allowed-tools: Bash(gh:*), Read, Edit
argument-hint: [이슈번호] [상태: in-progress|done|backlog]
---

# 이슈 상태 업데이트

이슈 상태를 변경하고 docs/project.md를 동기화한다.

## 워크플로우

1. GitHub에서 이슈 정보 조회: `gh issue view <번호> --json title,state,labels`
2. docs/project.md에서 해당 이슈 찾기
3. 상태에 따라 섹션 이동:
   - `in-progress`: Backlog → In Progress (시작일 기록)
   - `done`: In Progress → Done (종료일 기록)
   - `backlog`: In Progress → Backlog (시작일 제거)

## project.md 테이블 형식

### In Progress / Backlog
```markdown
| # | 제목 | 담당자 | 우선순위 | 크기 | 시작일 | 라벨 |
```

### Done
```markdown
| # | 제목 | 담당자 | 우선순위 | 크기 | 시작일 | 종료일 | 라벨 |
```

## 사용 예시

`/project-update 70 done` - 70번 이슈를 Done으로 이동
