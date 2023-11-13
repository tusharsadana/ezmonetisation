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


@channel_router.post("/")
async def add_channel(
    payload: ChannelIn,
    service: ChannelService = Depends(get_channel_service),
    session: AsyncSession = Depends(get_session),
):
    is_created, message = await service.add_channel(session, payload)
    if is_created:
        return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_200_OK
        )
    return ORJSONResponse(
            {"message": message}, status_code=status.HTTP_400_BAD_REQUEST
        )
