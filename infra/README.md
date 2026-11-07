# Infrastructure

로컬 개발 환경 구성만 관리합니다. 현재 운영 중인 원격 환경(스테이징/프로덕션)은 없습니다.

## 디렉토리 구조

```text
infra/
└── dev/
    └── docker-compose.yml      # 로컬 개발 환경 (DB, Redis, MinIO)
```

## 사용법

```bash
make infra-up    # 공유 로컬 인프라(db/redis/minio) 기동
make infra-down  # 공유 인프라 중지 (볼륨 데이터 보존)
make devup       # 공유 인프라 + backend/frontend 개발 서버 동시 구동
```
