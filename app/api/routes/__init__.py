from fastapi import APIRouter

from app.api.routes import ping, user

api_router = APIRouter()
api_router.include_router(user.app_router, prefix="/user", tags=["user"])
api_router.include_router(ping.app_router, prefix="/ping", tags=["ping"])
