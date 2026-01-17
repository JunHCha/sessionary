# Sessionary Projects

> 이 문서는 GitHub Projects에서 로컬로 마이그레이션된 프로젝트 관리 문서입니다.

## 프로젝트 관리 가이드

> 프로젝트 관리는 Claude Code의 `/project` skill을 통해 로컬에서 수행합니다.

### Claude Code Skill 명령어

| 명령어 | 설명 |
|--------|------|
| `/project draft-pr` | 현재 브랜치에서 Draft PR 생성 |
| `/project link-pr` | PR을 관련 이슈에 연결 |
| `/project update` | 이슈 상태 변경 및 project.md 업데이트 |
| `/project new-issue` | 새 이슈 생성 |
| `/project status` | 프로젝트 현황 조회 |

### 작업 흐름

1. **이슈 생성**: `/project new-issue`로 새 이슈를 생성합니다.
2. **브랜치 생성**: 이슈 번호를 포함한 브랜치를 생성합니다 (예: `123-feature-description`).
3. **Draft PR 생성**: `/project draft-pr`로 Draft PR을 생성합니다.
4. **작업 수행**: 드래프트 PR에서 필요한 작업을 수행합니다.
5. **리뷰 준비**: 작업이 완료되면 self code review를 진행한 뒤, "Ready for review" 상태로 변경합니다.
6. **PR-이슈 연결**: `/project link-pr`로 PR을 이슈에 연결합니다.
7. **코드 리뷰**: 팀원들이 PR을 리뷰하고 필요한 수정사항을 요청합니다.
8. **병합**: PR을 main 브랜치로 병합합니다.
9. **이슈 종료**: `/project update`로 이슈를 닫고 project.md를 업데이트합니다.

### 주의사항

- 브랜치 이름은 반드시 이슈 번호로 시작해야 합니다.
- PR을 "Ready for review" 상태로 변경하기 전에 작업이 완료되었는지 확인하세요.
- 이슈를 닫을 때는 `/project update`를 사용하여 종료 날짜를 기록하세요.

---

## 프로젝트 보드

### In Progress (진행 중)

| # | 제목 | 담당자 | 우선순위 | 크기 | 시작일 | 라벨 |
|---|------|--------|----------|------|--------|------|
| [#46](https://github.com/JunHCha/sessionary/issues/46) | 🖥️⚒️ 로그인 Modal 레이아웃 구현 | JunHCha | P2 | S | 2026-01-17 | feature |

### Backlog (대기)

| # | 제목 | 담당자 | 우선순위 | 크기 | 시작일 | 라벨 |
|---|------|--------|----------|------|--------|------|
| [#44](https://github.com/JunHCha/sessionary/issues/44) | 🖥️⚒️ UserInfo 컴포넌트 및 profile setting, plan info page 추가 | JunHCha | P2 | M | 2024-10-20 | feature |
| [#49](https://github.com/JunHCha/sessionary/issues/49) | 🖥️⚒️ Ticket Plan alert modal 레이아웃 구현 | JunHCha | P2 | S | 2024-10-20 | feature |
| [#52](https://github.com/JunHCha/sessionary/issues/52) | 🖥️⚒️ Session detail view 레이아웃 구현 | JunHCha | P2 | M | 2024-10-20 | feature |
| [#51](https://github.com/JunHCha/sessionary/issues/51) | 🖥️⚒️ 통합악보 viewer 레이아웃 구현 | JunHCha | P2 | M | 2024-10-20 | feature |
| [#55](https://github.com/JunHCha/sessionary/issues/55) | ⚙️🔧 google oauth redirect url을 외부 인자로 받을 수 있도록 수정 | JunHCha | P2 | L | 2024-10-21 | feature |

### Done (완료)

#### ✨ 2025-1Q 마일스톤

| # | 제목 | 담당자 | 우선순위 | 크기 | 시작일 | 종료일 | 라벨 |
|---|------|--------|----------|------|--------|--------|------|
| [#70](https://github.com/JunHCha/sessionary/issues/70) | ⚙️ ⚒️ 스트리밍 서버 구현 | JunHCha | P1 | XL | 2026-01-10 | 2026-01-16 | feature |
| [#48](https://github.com/JunHCha/sessionary/issues/48) | ⚙️⚒️ Ticket plan 차감 로직 구현 | JunHCha | P2 | M | 2024-10-20 | 2026-01-16 | feature |
| [#45](https://github.com/JunHCha/sessionary/issues/45) | 🖥️⚒️ Lecture Detail view 페이지 레이아웃 구현 | JunHCha | P2 | M | 2024-10-20 | 2026-01-10 | feature |
| [#47](https://github.com/JunHCha/sessionary/issues/47) | ⚙️⚒️ subscription history 모델 추가 | kor-kms | P2 | L | 2025-01-09 | 2025-10-11 | feature |
| [#50](https://github.com/JunHCha/sessionary/issues/50) | ⚙️⚒️ auth token 발급 로직 개편 | JunHCha, kor-kms | P2 | M | 2025-01-09 | 2025-01-22 | feature |
| [#58](https://github.com/JunHCha/sessionary/issues/58) | 🖥️🔧 logo 이미지 표시 오류 수정 | JunHCha | P3 | XS | 2024-12-15 | 2025-01-08 | fix |
| [#56](https://github.com/JunHCha/sessionary/issues/56) | 🖥️🔧 Flowbite로 레이아웃 디자인을 추가합니다. | JunHCha | P4 | M | 2024-11-04 | 2024-11-04 | fix |
| [#43](https://github.com/JunHCha/sessionary/issues/43) | 🖥️⚒️ 메인페이지 레이아웃 재배치 | JunHCha | P2 | S | 2024-10-21 | 2024-10-22 | feature |
| [#42](https://github.com/JunHCha/sessionary/issues/42) | ⚙️🧹 app model, schema 통합 | JunHCha | P2 | S | 2024-10-20 | 2024-10-21 | refactor |
| [#32](https://github.com/JunHCha/sessionary/issues/32) | ♺ Project, Issue, PR 생명주기를 수정합니다. | JunHCha | P3 | L | 2024-10-19 | 2024-10-19 | feature |
| [#40](https://github.com/JunHCha/sessionary/issues/40) | ♺🚨update project card 워크플로우를 수정합니다. | JunHCha | P1 | S | 2024-10-20 | 2024-10-20 | feature |

#### ♺ DevOps 세팅 마일스톤

| # | 제목 | 담당자 | 우선순위 | 크기 | 시작일 | 종료일 | 라벨 |
|---|------|--------|----------|------|--------|--------|------|
| [#26](https://github.com/JunHCha/sessionary/issues/26) | 🔎 Code review guide 문서화 | JunHCha | P2 | S | 2024-09-22 | 2024-10-04 | documentation |
| [#24](https://github.com/JunHCha/sessionary/issues/24) | ♺ Staging Frontend CD pipeline 구축 | JunHCha | P1 | M | 2024-09-30 | 2024-10-02 | feature |
| [#25](https://github.com/JunHCha/sessionary/issues/25) | 🚀 Github Projects 관리 Guide 문서화 | JunHCha | P1 | L | 2024-09-20 | 2024-10-20 | - |
| [#23](https://github.com/JunHCha/sessionary/issues/23) | ♺ Staging Backend CD pipeline 구축 | JunHCha | P1 | M | 2024-09-21 | 2024-10-02 | feature |

#### ✨Staging Deploy 마일스톤

| # | 제목 | 타입 | 담당자 | 우선순위 | 크기 |
|---|------|------|--------|----------|------|
| [#19](https://github.com/JunHCha/sessionary/pull/19) | ⚙️🧪 remove backend test codes' dependancies on Docker container | PR | JunHCha | P2 | M |
| [#18](https://github.com/JunHCha/sessionary/pull/18) | ✨ fly.io에 staging application을 배포합니다. | PR | JunHCha | P2 | M |
| [#17](https://github.com/JunHCha/sessionary/pull/17) | 🖥️🔧 setup api base url using server side rendering | PR | JunHCha | P2 | M |
| [#16](https://github.com/JunHCha/sessionary/pull/16) | ⚙️🔧 use google_oauth_redirect uri from setting instance | PR | JunHCha | P2 | M |
| [#15](https://github.com/JunHCha/sessionary/pull/15) | 🖥️ 홈페이지 레이아웃과 구글 로그인을 구현합니다. | PR | JunHCha | P2 | M |
| [#14](https://github.com/JunHCha/sessionary/pull/14) | 🎨 프론트엔드 소스를 추가하고 모노레포 구성을 적용합니다. | PR | JunHCha | P2 | M |
| [#13](https://github.com/JunHCha/sessionary/pull/13) | ⚒️ 강의정보를 불러오는 API를 추가합니다. | PR | JunHCha | P2 | M |
| [#12](https://github.com/JunHCha/sessionary/pull/12) | 🚀 인증 세션 스키마에 구독 정보를 추가합니다. | PR | JunHCha | P2 | M |
| [#11](https://github.com/JunHCha/sessionary/pull/11) | 🚀 인증 레디스 세션에 사용자 정보를 직접 저장합니다. | PR | JunHCha | P2 | M |
| [#10](https://github.com/JunHCha/sessionary/pull/10) | ⚒️ artist API를 추가합니다. | PR | JunHCha | P2 | M |
| [#9](https://github.com/JunHCha/sessionary/pull/9) | 🔐 token transport를 bearer header로 변경합니다. | PR | JunHCha | P2 | M |
| [#8](https://github.com/JunHCha/sessionary/pull/8) | 🏗️ test db container를 제거합니다. | PR | JunHCha | P2 | M |
| [#7](https://github.com/JunHCha/sessionary/pull/7) | 🔐 access token을 redis에 저장하도록 수정합니다. | PR | JunHCha | P2 | M |
| [#6](https://github.com/JunHCha/sessionary/pull/6) | ⚒️ table schema를 수정하고, async scoped session을 도입합니다. | PR | JunHCha | P2 | M |
| [#5](https://github.com/JunHCha/sessionary/pull/5) | 🔐 Google OAuth2 인증을 구현합니다. | PR | JunHCha | P2 | M |
| [#4](https://github.com/JunHCha/sessionary/pull/4) | 🔧 App이 실행되도록 수정합니다. | PR | JunHCha | P2 | M |
| [#3](https://github.com/JunHCha/sessionary/pull/3) | 🏗️ Initial Database migration을 추가합니다. | PR | JunHCha | P2 | M |
| [#2](https://github.com/JunHCha/sessionary/pull/2) | 🤖 ChatGPT 코드리뷰 봇을 추가합니다. | PR | JunHCha | P2 | M |
| [#1](https://github.com/JunHCha/sessionary/pull/1) | 🏗️🏭 Docker container 기반 개발환경을 설정합니다. | PR | JunHCha | P2 | M |

#### 기타 완료 항목

| # | 제목 | 타입 | 저장소 | 담당자 | 우선순위 | 크기 | 시작일 | 종료일 |
|---|------|------|--------|--------|----------|------|--------|--------|
| [#1](https://github.com/kor-kms/todo_fastapi/issues/1) | ⚒️ Todo REST API 구현 (Backend Onboarding) | Issue | todo_fastapi | JunHCha, kor-kms | P0 | S | 2024-08-01 | 2024-10-04 |
| [#1](https://github.com/kor-kms/todo_svelte/issues/1) | ⚒️ Todo Client 구현 (Frontend Onboarding) | Issue | todo_svelte | JunHCha, kor-kms | P0 | L | 2024-08-01 | 2024-10-04 |
| [#27](https://github.com/JunHCha/sessionary/pull/27) | ♺📝 update issue template | PR | sessionary | JunHCha | P3 | S | 2024-09-21 | - |
| [#28](https://github.com/JunHCha/sessionary/pull/28) | ♺ adjust staging machine resources | PR | sessionary | JunHCha | P1 | XS | 2024-09-22 | 2024-10-01 |
| [#29](https://github.com/JunHCha/sessionary/pull/29) | ♺ add staging CI/CD actions | PR | sessionary | JunHCha | P1 | S | 2024-09-25 | 2024-10-01 |
| [#30](https://github.com/JunHCha/sessionary/pull/30) | 🖥️♺ upgrade packages | PR | sessionary | JunHCha | P1 | XS | 2024-09-30 | 2024-10-02 |
| [#31](https://github.com/JunHCha/sessionary/pull/31) | ♺🚨 fix staging cd actions | PR | sessionary | JunHCha | P0 | XS | 2024-10-01 | 2024-10-02 |

---

## 마일스톤 목록

| 마일스톤 | 마감일 | 설명 |
|----------|--------|------|
| ✨ 2025-1Q | 2025-03-31 | 2025년 1분기 목표 |
| ♺ DevOps 세팅 | 2024-09-30 | DevOps 환경 구축 |
| ✨Staging Deploy | 2024-08-21 | Staging 환경 배포 |

---

## 우선순위 정의

| 우선순위 | 설명 |
|----------|------|
| P0 | 긴급 - 즉시 처리 필요 |
| P1 | 높음 - 빠른 처리 필요 |
| P2 | 중간 - 일반적인 우선순위 |
| P3 | 낮음 - 여유 있을 때 처리 |
| P4 | 최저 - 언제든 처리 가능 |

## 크기 정의

| 크기 | 설명 |
|------|------|
| XS | 매우 작음 (1-2 시간) |
| S | 작음 (반나절) |
| M | 중간 (1일) |
| L | 큼 (2-3일) |
| XL | 매우 큼 (1주 이상) |

---

*마지막 업데이트: 2026-01-17 (이슈 #46 In Progress)*
*원본: https://github.com/users/JunHCha/projects/2*
