#!/bin/bash
set -euo pipefail

cp infra/staging/fly-backend.toml backend/fly.toml

cd backend
flyctl deploy
