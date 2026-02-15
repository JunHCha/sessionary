# Infrastructure

Sessionary 프로젝트의 인프라 구성 및 관리 가이드입니다.

## 환경 구성

| 환경 | 플랫폼 | 설명 |
|------|--------|------|
| **Dev** | Docker Compose | 로컬 개발 환경 (`infra/dev/`) |
| **Staging** | Fly.io | 무료 범위 내 구성 (`infra/staging/`) |
| **Production** | TBD | 향후 IaaS(AWS/GCP) 전환 예정 (`infra/terraform/`) |

## 디렉토리 구조

```text
infra/
├── dev/
│   └── docker-compose.yml      # 로컬 개발 환경 (DB, Redis, MinIO)
├── staging/
│   ├── fly-backend.toml        # Backend Fly.io 설정
│   └── fly-frontend.toml       # Frontend Fly.io 설정
├── prod/                       # (예약)
├── terraform/
│   └── README.md               # Production IaaS 전환 시 사용
└── scripts/
    ├── deploy-staging-backend.sh    # Backend 배포 스크립트
    ├── deploy-staging-frontend.sh   # Frontend 배포 스크립트
    └── setup-staging-secrets.sh     # 시크릿 관리 runbook
```

## Staging 인프라

### 앱 구성

| 앱 | Fly.io 이름 | 리전 | 사양 |
|----|-------------|------|------|
| Backend | `sessionary-dawn-field-679` | NRT (도쿄) | shared-cpu-1x, 1GB RAM, 싱글 인스턴스 |
| Frontend | `staging-sessionary` | NRT (도쿄) | shared-cpu-1x, 1GB RAM, 싱글 인스턴스 |

### 외부 서비스

| 서비스 | 제공자 | 용도 |
|--------|--------|------|
| PostgreSQL | Supabase | 데이터베이스 |
| Redis | Upstash (Fly.io 제휴) | 세션 스토리지 |
| Object Storage | Tigris (Fly.io 통합) | 비디오 스토리지 |

### 시크릿 관리

Staging 시크릿은 `flyctl secrets`로 관리됩니다.

```bash
# 시크릿 목록 확인
flyctl secrets list -a sessionary-dawn-field-679
flyctl secrets list -a staging-sessionary

# 시크릿 설정 (runbook 참조)
./infra/scripts/setup-staging-secrets.sh
```

자세한 시크릿 목록과 설정 방법은 `infra/scripts/setup-staging-secrets.sh`를 참조하세요.

## 배포

### 자동 배포 (CI/CD)

GitHub Actions가 `main` 브랜치 push 시 자동 배포합니다:

- **Backend**: `backend/**` 또는 `infra/**` 변경 시 → `.github/workflows/deploy-staging-backend.yml`
- **Frontend**: `frontend/**` 또는 `infra/**` 변경 시 → `.github/workflows/deploy-staging-frontend.yml`

### 수동 배포

```bash
# Backend
flyctl deploy -a sessionary-dawn-field-679 --config infra/staging/fly-backend.toml --dockerfile backend/Dockerfile

# Frontend
flyctl deploy -a staging-sessionary --config infra/staging/fly-frontend.toml --dockerfile frontend/Dockerfile
```

### 롤백

```bash
# 릴리스 목록 확인
flyctl releases -a sessionary-dawn-field-679

# 특정 이미지로 롤백
flyctl deploy -a sessionary-dawn-field-679 --image <previous-image>
```

## Tigris Object Storage

Staging 비디오 스토리지로 Tigris (Fly.io 통합)를 사용합니다.

- S3 호환 API로 기존 MinIOVideoProvider를 그대로 사용
- `flyctl storage create`로 생성 및 관리
- 무료 범위: 5GB 스토리지, 10K 요청/월

```bash
# 스토리지 상태 확인
flyctl storage list -a sessionary-dawn-field-679
```

## Production 확장 계획

Production은 향후 AWS/GCP 등 IaaS로 전환 예정입니다.
`infra/terraform/`에 Terraform 구성을 추가할 예정이며, Staging은 Fly.io를 유지합니다.
