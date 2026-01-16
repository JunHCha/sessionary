---
description: 프로젝트 현황 조회
allowed-tools: Bash(gh:*), Bash(git:*), Read
---

# 프로젝트 현황 조회

현재 프로젝트 상태를 요약해서 보여준다.

## 워크플로우

1. docs/project.md 읽기
2. In Progress 항목 요약
3. Backlog 상위 항목 요약
4. 현재 브랜치와 연결된 이슈 정보 표시

## 출력 형식

```
## 현재 작업 중 (In Progress)
- #70 스트리밍 서버 구현 (P1, XL) - 2026-01-10 시작

## 대기 중 (Backlog 상위 3개)
- #71 비디오 플레이어 구현 (P1, L)
- #72 결제 연동 (P2, M)

## 현재 브랜치
- 브랜치: 70-스트리밍-서버-구현
- 연결된 이슈: #70
- PR 상태: Draft
```
