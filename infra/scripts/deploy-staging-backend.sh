#!/bin/bash

cp infra/staging/fly-backend.toml backend/fly.toml

cd backend
flyctl deploy
