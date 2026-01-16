---
description: PR을 관련 이슈에 연결하고 project.md 업데이트
allowed-tools: Bash(gh:*), Bash(git:*), Read, Edit
---

# PR-이슈 연결

현재 브랜치의 PR을 관련 이슈에 연결하고 docs/project.md를 업데이트한다.

## 워크플로우

1. 현재 브랜치의 PR 번호 확인: `gh pr view --json number,title,url`
2. 브랜치명에서 이슈 번호 추출
3. 이슈 본문에 PR 링크 추가:
   - `gh issue view <이슈번호> --json body -q .body`로 기존 본문 가져오기
   - 기존 본문에 PR 링크를 결합하여 새 본문 생성
   - `gh issue edit <이슈번호> --body "<결합된 전체 본문>"`로 업데이트 (주의: `--body`는 본문을 교체함)
4. docs/project.md의 해당 이슈 행에 PR 정보 추가
