# stdlib
import logging
from typing import Optional
from uuid import UUID

# thirdparty
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.monetization_service.core.db import get_session
from src.monetization_service.schemas.api.v1.video import VideoIn, VideoSelectIn
from src.monetization_service.services.auth import Authorized

from src.monetization_service.services.video.video import (
    VideoService,
    get_video_service
)

logger = logging.getLogger(__name__)

video_router = APIRouter(
    prefix="/video",
    tags=["Video"],
    dependencies=[Depends(Authorized(0, 1, 2))],
)


@video_router.post("/add-video")
async def add_video(
    payload: VideoIn,
    service: VideoService = Depends(get_video_service),
    session: AsyncSession = Depends(get_session),
):
    is_created, message = await service.add_video(session, payload)
    if is_created:
        return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_201_CREATED
        )
    return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_400_BAD_REQUEST
        )


@video_router.get("/{username}/get-video-list")
async def get_video_list(
    username: str,
    service: VideoService = Depends(get_video_service),
    session: AsyncSession = Depends(get_session),
):
    is_valid, data = await service.get_video_list(session, username)
    if is_valid:
        return ORJSONResponse(
            data, status_code=status.HTTP_200_OK
        )
    return ORJSONResponse(
            {"message": data}, status_code=status.HTTP_400_BAD_REQUEST
        )


@video_router.put("/activate-videos")
async def activate_videos(
    payload: VideoSelectIn,
    service: VideoService = Depends(get_video_service),
    session: AsyncSession = Depends(get_session),
):
    is_updated, message = await service.activate_videos(session, payload)
    if is_updated:
        return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_200_OK
        )
    return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_400_BAD_REQUEST
        )
