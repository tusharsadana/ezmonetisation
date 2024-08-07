from fastapi import APIRouter

from src.monetization_service.api.v1.auth import auth_router
from src.monetization_service.api.v1.channel import channel_router
from src.monetization_service.api.v1.video import video_router
from src.monetization_service.api.v1.dashboard import dashboard_router
v1_router = APIRouter(prefix="/v1")

v1_router.include_router(dashboard_router)
v1_router.include_router(channel_router)
v1_router.include_router(video_router)
v1_router.include_router(auth_router)


