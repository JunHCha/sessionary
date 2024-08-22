set +ex

env
alembic upgrade head
uvicorn --host 0.0.0.0 app.main:app --port 10080 --workers 3
