from fastapi import APIRouter, Depends

from app.auth.access import authenticated_user
from app.db.tables import User
from app.user.models import UserRead

app_router = APIRouter()


@app_router.get("")
async def pong():
    return {"ping": "pong!"}


@app_router.get("/auth")
async def auth_pong(user: User = Depends(authenticated_user)):
    return {"ping": "pong!", "data": UserRead.model_validate(user)}
