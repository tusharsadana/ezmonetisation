# stdlib
import logging
from uuid import UUID

# thirdparty
import stripe
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import ORJSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.monetization_service.core.db import get_session
# from src.monetization_service.schemas.api.v1.channel import ChannelIn, ChannelSubIn
from src.monetization_service.services.auth import Authorized

from src.monetization_service.services.payment.payment import (
    PaymentService,
    get_payment_service
)

logger = logging.getLogger(__name__)

payment_router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
    dependencies=[Depends(Authorized(0, 1, 2))],
)


@payment_router.post("/create-checkout-session")
async def create_checkout_session(
        price_id: str,
        success_url: str,
        cancel_url: str,
        user_email: str,
        quantity: int,
        service: PaymentService = Depends(get_payment_service),
        session: AsyncSession = Depends(get_session)
):
    is_created, content = await service.create_checkout_session(session, price_id, quantity, success_url, cancel_url, user_email)
    if is_created:
        return RedirectResponse(content, status_code=303)

    return ORJSONResponse({"error": content}, status_code=status.HTTP_400_BAD_REQUEST)


@payment_router.post("/stripe-webhook")
async def webhook_received(
        request: Request,
        service: PaymentService = Depends(get_payment_service),
        session: AsyncSession = Depends(get_session)
):
    success, data, message = await service.stripe_webhook(session, request)

    if success:
        return ORJSONResponse({"message": message, "data": data}, status_code=status.HTTP_200_OK)
    if data:
        return ORJSONResponse({"message": message, "data": data}, status_code=status.HTTP_400_BAD_REQUEST)

    return ORJSONResponse({"message": message}, status_code=status.HTTP_400_BAD_REQUEST)


@payment_router.post("/create-portal-session")
async def create_portal_session(
        customer_id: str,
        return_url: str,
        service: PaymentService = Depends(get_payment_service)
):

    is_created, content = await service.create_portal_session(customer_id, return_url)
    if is_created:
        return ORJSONResponse({"url": content}, status_code=status.HTTP_200_OK)

    return ORJSONResponse({"error": content}, status_code=status.HTTP_400_BAD_REQUEST)
