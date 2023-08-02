from fastapi import APIRouter

from . import auth, ping

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
