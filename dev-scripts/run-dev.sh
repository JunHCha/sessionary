set +ex

docker compose up -d

uvicorn --env-file ./.env.dev --host 0.0.0.0 --port 8000 app.main:app --reload

docker compose down
