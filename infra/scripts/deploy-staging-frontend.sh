#!/bin/bash
set -euo pipefail

cp infra/staging/fly-frontend.toml frontend/fly.toml

cd frontend
flyctl deploy
