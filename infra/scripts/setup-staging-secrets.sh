#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Sessionary Staging Secrets Management Runbook
# =============================================================================
#
# 이 스크립트는 Staging 환경의 시크릿 관리를 위한 참조 문서(runbook)입니다.
# 실행 전 placeholder 값(<...>)을 실제 값으로 교체하세요.
#
# 사전 요구사항:
#   - flyctl CLI 설치 (https://fly.io/docs/flyctl/install/)
#   - flyctl auth login 완료
#
# 롤백 절차:
#   flyctl releases -a sessionary-dawn-field-679
#   flyctl deploy -a sessionary-dawn-field-679 --image <previous-image>
#
# =============================================================================

echo "============================================"
echo " Sessionary Staging Secrets Setup"
echo "============================================"
echo ""
echo "WARNING: placeholder 값(<...>)을 실제 값으로 교체한 후 실행하세요."
echo ""

# -----------------------------------------------------------------------------
# Backend: sessionary-dawn-field-679
# -----------------------------------------------------------------------------
echo "[Backend] Setting secrets for sessionary-dawn-field-679..."

flyctl secrets set -a sessionary-dawn-field-679 \
  APP_ENV="staging" \
  SECRET_KEY="<your-secret-key>" \
  DATABASE_URL="<your-database-url>" \
  AUTH_REDIS_URL="<your-redis-url>" \
  GOOGLE_CLIENT_ID="<your-google-client-id>" \
  GOOGLE_CLIENT_SECRET="<your-google-client-secret>" \
  GOOGLE_OAUTH_REDIRECT_URI="https://staging.sessionary.n-e.kr/oauth-callback" \
  ALLOWED_HOSTS_STR="http://localhost,http://localhost:5173,http://127.0.0.1,https://staging.sessionary.n-e.kr" \
  COOKIE_NAME="satk" \
  COOKIE_DOMAIN=".sessionary.n-e.kr" \
  AUTH_SESSION_EXPIRE_SECONDS="36000" \
  AUTH_SESSION_REFRESH_INTERVAL="1800" \
  VIDEO_PROVIDER="local" \
  VIDEO_STORAGE_ENDPOINT="<tigris-endpoint>" \
  VIDEO_STORAGE_ACCESS_KEY="<tigris-access-key>" \
  VIDEO_STORAGE_SECRET_KEY="<tigris-secret-key>" \
  VIDEO_STORAGE_BUCKET_NAME="<tigris-bucket-name>" \
  VIDEO_STORAGE_SECURE="true"

echo "[Backend] Done. Verifying..."
flyctl secrets list -a sessionary-dawn-field-679

echo ""

# -----------------------------------------------------------------------------
# Frontend: staging-sessionary
# -----------------------------------------------------------------------------
echo "[Frontend] Setting secrets for staging-sessionary..."

flyctl secrets set -a staging-sessionary \
  PUBLIC_API_BASE_URL="https://staging-api.sessionary.n-e.kr"

echo "[Frontend] Done. Verifying..."
flyctl secrets list -a staging-sessionary

echo ""
echo "============================================"
echo " All secrets configured successfully!"
echo "============================================"
