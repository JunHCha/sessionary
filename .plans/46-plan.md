# Issue #46 해결 계획서

> 생성일: 2026-01-17
> 이슈: [🖥️⚒️ 로그인 Modal 레이아웃 구현](https://github.com/JunHCha/sessionary/issues/46)

## 1. 문제 정의

### 1.1 현재 상황
- `LoginButton.svelte` 컴포넌트 내부에 Modal이 포함되어 있음
- Modal은 Flowbite의 기본 스타일을 사용 중
- message나 redirect URL을 외부에서 전달할 수 없는 구조
- 로그인 성공 후 항상 `/home`으로 이동함

### 1.2 해결하고자 하는 문제
- 로그인 Modal을 독립적인 컴포넌트로 분리
- 외부에서 `message`와 `redirectUrl`을 파라미터로 전달 가능하게 함
- 프로젝트 디자인 토큰에 맞는 스타일 적용

### 1.3 기대 결과
- 재사용 가능한 `LoginModal` 컴포넌트 생성
- 다양한 상황에서 맞춤 메시지와 리다이렉트 경로 지정 가능
- 프로젝트 디자인 시스템과 일관된 UI

## 2. 해결 방안

### 2.1 접근 방식
1. `LoginModal.svelte` 컴포넌트를 새로 생성
2. `message`와 `redirectUrl`을 props로 받음
3. `redirectUrl`은 sessionStorage에 저장하여 OAuth 콜백 후 처리
4. 디자인 토큰(#FF5C16, #0C0C0C 등)을 활용한 커스텀 스타일 적용

### 2.2 구현 세부사항

**LoginModal 컴포넌트 구조:**
```svelte
<script lang="ts">
  interface Props {
    open: boolean;
    message?: string;
    redirectUrl?: string;
  }

  let { open = $bindable(), message = "로그인이 필요합니다", redirectUrl = "/home" }: Props = $props();
</script>
```

**sessionStorage 활용:**
- 로그인 버튼 클릭 시 `sessionStorage.setItem('redirectUrl', redirectUrl)`
- OAuth 콜백 페이지에서 `sessionStorage.getItem('redirectUrl')` 후 해당 경로로 이동

### 2.3 의사결정 사항
| 항목 | 결정 내용 | 이유 |
|------|----------|------|
| 컴포넌트 분리 | LoginModal을 독립 컴포넌트로 분리 | 재사용성 향상 및 관심사 분리 |
| Redirect 처리 | sessionStorage 사용 | OAuth 흐름 상 클라이언트에서 간단히 처리 가능, 백엔드 수정 불필요 |
| 디자인 | 프로젝트 디자인 토큰 사용 | UI 일관성 유지 |

## 3. 영향받는 파일

### 3.1 수정 대상
| 파일 경로 | 변경 내용 |
|----------|----------|
| `frontend/src/lib/features/auth/components/LoginButton.svelte` | Modal 코드 제거, LoginModal 사용으로 변경 |
| `frontend/src/lib/features/auth/index.ts` | LoginModal export 추가 |
| `frontend/src/routes/oauth-callback/+page.svelte` | sessionStorage에서 redirectUrl 읽어 처리 |

### 3.2 신규 생성
| 파일 경로 | 용도 |
|----------|------|
| `frontend/src/lib/features/auth/components/LoginModal.svelte` | 독립적인 로그인 모달 컴포넌트 |

## 4. 테스트 전략

### 4.1 테스트 범위
- LoginModal 컴포넌트 렌더링 테스트
- props 전달 테스트 (message, redirectUrl)
- sessionStorage 저장/읽기 테스트

### 4.2 테스트 케이스
| 케이스 | 타입 | 설명 |
|--------|------|------|
| 기본 메시지로 모달 렌더링 | approval | message prop 없이 기본값으로 렌더링 확인 |
| 커스텀 메시지 렌더링 | edge_case | message prop 전달 시 해당 메시지 표시 |
| redirectUrl sessionStorage 저장 | edge_case | 로그인 버튼 클릭 시 redirectUrl이 sessionStorage에 저장됨 |
| 빈 redirectUrl 처리 | edge_case | redirectUrl이 없을 때 기본값 "/home" 사용 |

### 4.3 테스트 파일
| 파일 경로 | 테스트 대상 |
|----------|------------|
| `frontend/src/lib/features/auth/components/LoginModal.test.ts` | LoginModal 컴포넌트 |

## 5. 작업 체크리스트

- [ ] Phase 1: LoginModal 컴포넌트 생성
  - [ ] `LoginModal.svelte` 파일 생성
  - [ ] props 정의 (open, message, redirectUrl)
  - [ ] 디자인 토큰 기반 스타일 적용
  - [ ] Google 로그인 버튼 구현
  - [ ] sessionStorage에 redirectUrl 저장 로직
- [ ] Phase 2: 기존 코드 수정
  - [ ] `LoginButton.svelte`에서 Modal 코드 제거
  - [ ] `LoginButton.svelte`에서 LoginModal 사용
  - [ ] `index.ts`에 LoginModal export 추가
- [ ] Phase 3: OAuth 콜백 처리
  - [ ] `oauth-callback/+page.svelte`에서 sessionStorage 읽기
  - [ ] redirectUrl로 이동하도록 수정
- [ ] Phase 4: 테스트
  - [ ] LoginModal 테스트 파일 생성
  - [ ] 테스트 케이스 작성 및 실행

## 6. 관련 문서

- spec 문서: `docs/spec/design/design-tokens.md`
- 관련 이슈: 없음
