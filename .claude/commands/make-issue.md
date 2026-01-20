---
description: 이슈 생성 또는 기존 이슈에 계획서 보강
argument-hint: <issue-number | 자연어 요구사항>
---

# Issue Maker

입력: $ARGUMENTS

## 분기 판단

- 숫자 입력 → 기존 이슈 조회: `gh issue view $ARGUMENTS --json title,body,labels`
- 그 외 → 새 이슈 생성

---

## 반복 사이클: 연구 → 계획 → 승인

최종 승인이 될 때까지 아래 사이클을 반복한다.

### 1단계: 연구

**목표**: 사실에 기반한 자료 수집. 추측이나 가정 금지.

수행 항목:
1. **사용자 요구사항 정리** (가장 중요한 진실)
   - 사용자가 명시한 요구사항을 원문 그대로 기록
   - 요구사항의 핵심 목표와 제약조건 파악
   - 불명확한 부분은 AskUserQuestion으로 즉시 확인

2. **코드베이스 분석**
   - Grep/Glob으로 관련 코드 탐색
   - 현재 구현 상태, 사용 중인 패턴, 의존성 파악
   - 실제 코드를 읽고 동작 방식 확인

3. **도메인 지식 수집**
   - `/spec-loader`로 관련 spec 문서 로드
   - 필요시 WebSearch로 real world example, 업계 표준, 베스트 프랙티스 조사

4. **연구 결과 파일 저장**
   - 기존 이슈: `.claude/tmp/research-{issue-number}.md`에 저장
   - 신규 이슈: `.claude/tmp/research-{timestamp}.md`로 임시 저장 (예: `research-20250121-143052.md`)
   - 이슈 생성 후: `.claude/tmp/research-{issue-number}.md`로 리네임
   - **요구사항 섹션을 최상단에 배치**
   - 발견한 사실만 나열 (출처 명시)
   - 불확실한 부분은 "확인 필요"로 표시
   - 피드백 반영 시 파일 업데이트

### 2단계: 계획

**목표**: 연구 결과를 근거로 해결 방안 수립

수행 항목:
1. **연구 파일 참조**
   - `.claude/tmp/research-{issue-number}.md` 또는 임시 파일 읽어서 근거 확보

2. **방안 선택**
   - 가능한 접근 방식 나열
   - 각 방식의 장단점 비교
   - 선택한 방안과 그 근거 명시

3. **의사결정 정리**
   - 결정된 사항: 근거와 함께 기록
   - 모호한 사항: AskUserQuestion으로 질문

4. **계획서 초안 작성** (하단 템플릿 참조)

### 3단계: 승인

계획서를 사용자에게 제시하고 검토 요청.

- **승인** → 이슈 생성/수정 후 종료
- **피드백** → 연구 파일 업데이트 후 1단계부터 다시 시작. 승인될 때까지 반복.

```bash
# 새 이슈
gh issue create --title "{제목}" --body "{계획서}"
# 기존 이슈
gh issue edit $ARGUMENTS --body "{계획서}"
# Project 추가
gh project item-add <PROJECT_NUMBER> --owner @me --url <이슈URL>
```

---

## 계획서 템플릿

`.github/ISSUE_TEMPLATE/⚒️-tech-issue.md` 파일을 참조하여 작성한다.

---

## 출력

- 생성/수정된 이슈 번호
- 다음 단계: `/resolve-issue {이슈번호}`
