from fastapi import APIRouter

from . import auth

app_router = APIRouter()
app_router.include_router(auth.router)
