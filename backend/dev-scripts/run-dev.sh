set +ex

uv run alembic upgrade head
uv run uvicorn --host 0.0.0.0 --port 8000 app.main:get_app --reload --factory
