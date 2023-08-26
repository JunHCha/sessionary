from fastapi import APIRouter

app_router = APIRouter()


@app_router.get("")
async def pong():
    return {"ping": "pong!"}
