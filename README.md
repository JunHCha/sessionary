# Sessionary

## 소개
Sessionary는 워십/밴드 세션에 초점을 맞춘 온라인 강의 서비스입니다.
음악가와 워십 리더에게 차별화된 학습 경험을 제공하며, 음악 실력과 지식을 키울 수 있는 다양한 강의와 리소스를 제공합니다.

## 모노레포

- `frontend/` — SvelteKit (yarn)
- `backend/` — FastAPI (uv)

서로 다른 툴체인을 루트에서 한 번에 다루기 위한 `make` 명령을 제공한다.

```bash
make install      # fe/be 의존성 설치
make test         # 백엔드 + 프론트 전체 테스트
make test-e2e     # 프론트 E2E (백엔드는 mock)
make gen-client   # OpenAPI 스냅샷 + API client 재생성
make check-spec   # fe/be 계약 drift 검증
make help         # 전체 명령
```

- 테스트 전략(계층 책임 / mock): [docs/testing.md](docs/testing.md)
- 빌드·실행 상세: [docs/domain/build-test.md](docs/domain/build-test.md)
