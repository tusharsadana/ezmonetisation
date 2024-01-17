# stdlib
import logging
from typing import Optional
from uuid import UUID

# thirdparty
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse, Response, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.monetization_service.core.db import get_session
from src.monetization_service.schemas.api.v1.dashboard import DateFilter
from src.monetization_service.services.auth import Authorized

from src.monetization_service.services.dashboard.dashboard import (
    DashboardService,
    get_dashboard_service
)

logger = logging.getLogger(__name__)

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(Authorized(0, 1, 2))],
)


@dashboard_router.get("/subscribers-earned-graph")
async def subscribers_earned_graph(
    user_email: str,
    date_filter: DateFilter = Depends(),
    service: DashboardService = Depends(get_dashboard_service),
    session: AsyncSession = Depends(get_session),
):
    is_created, output = await service.subscriber_earn_graph(session, user_email, date_filter)
    if is_created:
        return ORJSONResponse(output, status_code=status.HTTP_200_OK)
    return ORJSONResponse(
            {"message": output}, status_code=status.HTTP_400_BAD_REQUEST
        )


@dashboard_router.get("/watch-hours-earned-graph")
async def watch_hours_earned_graph(
    user_email: str,
    date_filter: DateFilter = Depends(),
    service: DashboardService = Depends(get_dashboard_service),
    session: AsyncSession = Depends(get_session),
):
    is_created, output = await service.watch_hour_earn_graph(session, user_email, date_filter)
    if is_created:
        return ORJSONResponse(output, status_code=status.HTTP_200_OK)
    return ORJSONResponse(
            {"message": output}, status_code=status.HTTP_400_BAD_REQUEST
        )
