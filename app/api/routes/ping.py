from fastapi import APIRouter, Depends

from app.core.auth.backend_builder import current_active_user
from app.db.tables import User

app_router = APIRouter()


@app_router.get("")
async def pong():
    return {"ping": "pong!"}


@app_router.get("/auth")
async def auth_pong(user: User = Depends(current_active_user)):
    return {"ping": "pong!", "data": user}
