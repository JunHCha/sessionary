# Sessionary

## Description
Sessionary is an online lecture service focusing on worship/band sessions.
Our platform provides a unique learning experience for musicians and worship leaders, offering a variety of courses and resources to enhance musical skills and knowledge.

## Monorepo

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
