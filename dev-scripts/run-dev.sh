set +ex

export APP_ENV=dev
export DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/sessionary

docker compose up -d

alembic upgrade head
uvicorn --host 0.0.0.0 --port 8000 app.main:app --reload

docker compose down
