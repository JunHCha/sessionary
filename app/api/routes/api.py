from fastapi import APIRouter

from app.api.routes import ping

api_router = APIRouter()
api_router.include_router(ping.router, tags=["ping"])
