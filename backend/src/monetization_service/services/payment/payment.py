from sqlalchemy.ext.asyncio import AsyncSession
from functools import cache
import stripe
from fastapi import Request
from datetime import datetime, timedelta

from src.monetization_service.models.user import Subscriptions
from src.monetization_service.queries.subscription import user_in_subscription, update_user_type, subscribe_user
from src.monetization_service.queries.users import user_exists
from src.monetization_service.queries.table import insert_to_table_by_model

stripe_secret_key = "sk_test_tR3PYbcVNZZ796tH88S4VQ2u"
webhook_secret_key = '{{STRIPE_WEBHOOK_SECRET}}'


class PaymentService:

    @staticmethod
    async def create_checkout_session(price_id: str, quantity: int, success_url: str, cancel_url: str):
        stripe.api_key = stripe_secret_key
        try:
            session = stripe.checkout.Session.create(
                success_url=success_url,
                cancel_url=cancel_url,
                line_items=[{"price": price_id, "quantity": quantity}],
                mode="payment",
            )
            return True, session.id

        except stripe.error.StripeError as e:
            return False, str(e)

    @staticmethod
    async def create_portal_session(customer_id: str, return_url: str):
        stripe.api_key = stripe_secret_key
        try:
            portal_session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            return True, portal_session.url

        except stripe.error.StripeError as e:
            return False, str(e)

    @staticmethod
    async def stripe_webhook(session: AsyncSession,user_email: str, request: Request):
        query = user_exists(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, None, "Invalid user_email"

        stripe.api_key = stripe_secret_key
        webhook_secret = webhook_secret_key
        try:
            payload = await request.body()
            sig_header = request.headers.get('Stripe-Signature')

            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )

            data = event['data']
            event_type = event['type']

            if event_type == 'checkout.session.completed':
                return True, data, "Checkout session completed"

            elif event_type == 'invoice.paid':
                query = update_user_type(user_email, 2)
                await session.execute(query)

                query = user_in_subscription(user_email)
                result = await session.execute(query)
                result = result.all()
                if len(result):
                    data = result[0]
                    if data[0]:
                        expiry = data[1] + timedelta(days=30)
                    else:
                        expiry = datetime.now() + timedelta(days=30)

                    query = subscribe_user(user_email, True, expiry)
                    await session.execute(query)
                else:
                    expiry = datetime.now() + timedelta(days=30)
                    insert_query = insert_to_table_by_model(
                        Subscriptions, {"user_email": user_email, "is_subscribed": True, "subscription_expiry": expiry}
                    )
                    await session.execute(insert_query)

                await session.commit()

                return True, data, "Invoice paid"

            elif event_type == 'invoice.payment_failed':
                return False, data, "Invoice payment failed"
            else:
                return False, None, ('Unhandled event type {}'.format(event_type))

        except stripe.error.SignatureVerificationError as e:
            return False, None, str(e)


@cache
def get_payment_service() -> PaymentService:
    return PaymentService()
