from uuid import UUID

# thirdparty
from sqlalchemy import (
    Delete,
    Insert,
    Select,
    UnaryExpression,
    Update,
    distinct,
    insert,
    select,
    update,
)
from sqlalchemy.sql import nullslast, and_
from sqlalchemy.sql.functions import count, func
from src.monetization_service.models.channel import WatchHourCredit, SubscriberCredit


def user_in_watch_credit(user_email: str):
    query = (
        select(WatchHourCredit.user_email)
        .where(WatchHourCredit.user_email == user_email)
    )
    return query


def update_watch_credit(user_email: str, credit: float):
    query = (
        update(WatchHourCredit)
        .where(WatchHourCredit.user_email == user_email)
        .values(watch_hour=WatchHourCredit.watch_hour + credit)
    )
    return query


def user_in_sub_credit(user_email: str):
    query = (
        select(SubscriberCredit.user_email)
        .where(SubscriberCredit.user_email == user_email)
    )
    return query


def update_sub_credit(user_email: str, credit: float):
    query = (
        update(SubscriberCredit)
        .where(SubscriberCredit.user_email == user_email)
        .values(subscriber_earn=SubscriberCredit.subscriber_earn + credit)
    )
    return query
