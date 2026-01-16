---
description: 새 GitHub 이슈 생성 및 project.md에 추가
allowed-tools: Bash(gh:*), Bash(git:*), Read, Edit
argument-hint: [제목]
---

# 새 이슈 생성

새 GitHub 이슈를 생성하고 docs/project.md Backlog에 추가한다.

## 워크플로우

1. 이슈 정보 수집 (제목, 라벨, 우선순위, 크기)
2. GitHub 이슈 생성: `gh issue create --title "<제목>" --label "<라벨>"`
3. docs/project.md Backlog 테이블에 추가
4. 브랜치 생성 여부 확인 후 생성: `git checkout -b <이슈번호>-<슬러그>`

## 이슈 제목 형식

| 접두사 | 의미 |
|--------|------|
| ⚙️ | 백엔드 |
| 🖥️ | 프론트엔드 |
| ⚒️ | 기능 구현 |
| 🔧 | 수정/버그픽스 |
| 🧹 | 리팩토링 |
| ♺ | DevOps/인프라 |

예시: `⚙️⚒️ Ticket plan 차감 로직 구현`

## 우선순위 및 크기

| 우선순위 | 설명 | 크기 | 설명 |
|----------|------|------|------|
| P0 | 긴급 | XS | 1-2시간 |
| P1 | 높음 | S | 반나절 |
| P2 | 중간 | M | 1일 |
| P3 | 낮음 | L | 2-3일 |
| P4 | 최저 | XL | 1주 이상 |

## 사용 예시

`/project-new-issue ⚙️⚒️ 비디오 트랜스코딩 구현`
