set +ex

uv run alembic upgrade head
uv run uvicorn --host 0.0.0.0 app.main:get_app --port 10080 --factory --workers 1
