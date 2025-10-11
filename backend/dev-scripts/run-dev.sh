set +ex

env
docker compose up -d

uv run alembic upgrade head
uv run uvicorn --host 0.0.0.0 --port 8000 app.main:app --reload

docker compose down
