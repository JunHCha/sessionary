# Production Terraform Configuration

> 현재 Staging은 `fly.toml` + `flyctl` + GitHub Actions로 관리됩니다.
> Fly.io Terraform provider는 2024년 3월 아카이브되어 공식 비권장입니다.

## 언제 사용하나요?

Production IaaS(AWS, GCP 등)로 전환할 때 이 디렉토리에 Terraform 구성을 추가합니다.

## 예상 구조

```
terraform/
├── modules/
│   ├── compute/        # ECS, Cloud Run 등
│   ├── storage/        # S3, GCS 등
│   ├── networking/     # VPC, Load Balancer 등
│   └── database/       # RDS, Cloud SQL 등
└── environments/
    └── prod/
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        └── terraform.tfvars
```

## 참고

- Staging: Fly.io (fly.toml + flyctl) - `infra/staging/` 참조
- Production: TBD - 이 디렉토리에 구성 예정
