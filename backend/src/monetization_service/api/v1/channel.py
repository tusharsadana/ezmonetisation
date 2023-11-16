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
from src.monetization_service.schemas.api.v1.channel import ChannelIn
from src.monetization_service.services.auth import Authorized

from src.monetization_service.services.channel.channel import (
    ChannelService,
    get_channel_service
)

logger = logging.getLogger(__name__)

channel_router = APIRouter(
    prefix="/channel",
    tags=["Channel"],
    dependencies=[Depends(Authorized(0, 1, 2))],
)


@channel_router.post("/add-channel")
async def add_channel(
    payload: ChannelIn,
    service: ChannelService = Depends(get_channel_service),
    session: AsyncSession = Depends(get_session),
):
    is_created, message = await service.add_channel(session, payload)
    if is_created:
        return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_201_CREATED
        )
    return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_400_BAD_REQUEST
        )


@channel_router.get("/{user_email}/get-channel-list")
async def get_channel_list(
    user_email: str,
    service: ChannelService = Depends(get_channel_service),
    session: AsyncSession = Depends(get_session),
):
    is_valid, data = await service.get_channel_list(session, user_email)
    if is_valid:
        return ORJSONResponse(
            data, status_code=status.HTTP_200_OK
        )
    return ORJSONResponse(
            {"message": data}, status_code=status.HTTP_400_BAD_REQUEST
        )


@channel_router.put("/{channel_id}/select-channel")
async def select_channel(
    channel_id: UUID,
    service: ChannelService = Depends(get_channel_service),
    session: AsyncSession = Depends(get_session),
):
    is_updated, message = await service.select_channel(session, channel_id)
    if is_updated:
        return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_200_OK
        )
    return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_400_BAD_REQUEST
        )
