set +ex

env
uv run alembic upgrade head
uv run uvicorn --host 0.0.0.0 app.main:app --port 10080 --workers 3
