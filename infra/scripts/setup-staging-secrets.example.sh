#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Sessionary Staging Secrets Management Runbook
# =============================================================================
#
# 사용법:
#   1. 이 파일을 복사: cp setup-staging-secrets.example.sh setup-staging-secrets.sh
#   2. setup-staging-secrets.sh의 placeholder(<...>)를 실제 값으로 교체
#   3. 실행: bash setup-staging-secrets.sh
#
# 사전 요구사항:
#   - flyctl CLI 설치 (https://fly.io/docs/flyctl/install/)
#   - flyctl auth login 완료
#
# 롤백 절차:
#   flyctl releases -a sessionary-staging-backend
#   flyctl deploy -a sessionary-staging-backend --image <previous-image>
#
# =============================================================================

echo "============================================"
echo " Sessionary Staging Secrets Setup"
echo "============================================"
echo ""
echo "WARNING: placeholder 값(<...>)을 실제 값으로 교체한 후 실행하세요."
echo ""

# 플레이스홀더 잔존 검사
if grep -v '^\s*#' "$0" | grep -v 'echo' | grep -q '<.*>'; then
  echo "ERROR: 스크립트에 교체되지 않은 placeholder(<...>)가 남아 있습니다."
  echo "placeholder를 실제 값으로 교체한 후 다시 실행하세요."
  exit 1
fi

# -----------------------------------------------------------------------------
# Backend: sessionary-staging-backend
# -----------------------------------------------------------------------------
echo "[Backend] Setting secrets for sessionary-staging-backend..."

flyctl secrets set -a sessionary-staging-backend \
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
flyctl secrets list -a sessionary-staging-backend

echo ""

# -----------------------------------------------------------------------------
# Frontend: sessionary-staging-frontend
# -----------------------------------------------------------------------------
echo "[Frontend] Setting secrets for sessionary-staging-frontend..."

flyctl secrets set -a sessionary-staging-frontend \
  PUBLIC_API_BASE_URL="https://staging-api.sessionary.n-e.kr"

echo "[Frontend] Done. Verifying..."
flyctl secrets list -a sessionary-staging-frontend

echo ""
echo "============================================"
echo " All secrets configured successfully!"
echo "============================================"
