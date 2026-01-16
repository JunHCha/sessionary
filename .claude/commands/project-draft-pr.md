---
description: 현재 브랜치에서 Draft PR 생성
allowed-tools: Bash(gh:*), Bash(git:*)
---

# Draft PR 생성

현재 브랜치에서 Draft PR을 생성한다.

## 워크플로우

1. 현재 브랜치명에서 이슈 번호 추출 (예: `70-스트리밍-서버-구현` → `70`)
2. GitHub에서 이슈 정보 조회: `gh issue view <번호> --json title,body,labels`
3. Draft PR 생성: `gh pr create --draft`

## 이슈 제목 형식

| 접두사 | 의미 |
|--------|------|
| ⚙️ | 백엔드 |
| 🖥️ | 프론트엔드 |
| ⚒️ | 기능 구현 |
| 🔧 | 수정/버그픽스 |
| 🧹 | 리팩토링 |
| ♺ | DevOps/인프라 |

## PR 본문 템플릿

```markdown
## Summary
- <변경사항 요약>

## Related Issue
Resolves #<이슈번호>

## Test Plan
- [ ] 테스트 항목
```
