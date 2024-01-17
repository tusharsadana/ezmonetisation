from sqlalchemy import Insert, Update, insert, update, select, and_, Delete
from sqlalchemy.sql.functions import func
from datetime import datetime
# project
from src.monetization_service.models.user import User, Subscriptions


def user_in_subscription(user_email: str):
    query = (select(Subscriptions.is_subscribed, Subscriptions.subscription_expiry).where(Subscriptions.user_email == user_email))
    return query


def update_user_type(user_email: str, user_type: int):
    query = (
        update(User)
        .values({"user_type": user_type})
        .where(User.email == user_email)
    )

    return query


def subscribe_user(user_email: str, is_subscribed: bool, expiry: datetime = None):
    update_values = {"is_subscribed": is_subscribed}

    if expiry is not None:
        update_values["subscription_expiry"] = expiry

    query = (
        update(Subscriptions)
        .values(update_values)
        .where(Subscriptions.user_email == user_email)
    )

    return query


