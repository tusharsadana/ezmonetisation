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
from datetime import datetime, timedelta

from sqlalchemy.sql import nullslast, and_
from sqlalchemy.sql.functions import count, func
from src.monetization_service.models.channel import WatchHourCredit, SubscriberCredit, SubscriberEarn, WatchHourEarn
from src.monetization_service.schemas.api.v1.dashboard import TimePeriodEnum


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


# def subscriber_log(user_email: str):
#     query = (
#         select(SubscriberEarn.subscriber_earn, SubscriberEarn.created_at)
#         .where(SubscriberEarn.user_email == user_email)
#     )
#     return query

def subscriber_log(user_email: str, time_period: TimePeriodEnum):
    base_query = select(SubscriberEarn.subscriber_earn, SubscriberEarn.created_at).where(
        SubscriberEarn.user_email == user_email
    )

    now = datetime.now()
    if time_period == TimePeriodEnum.DAY:
        time_filter = SubscriberEarn.created_at >= now - timedelta(days=1)
    elif time_period == TimePeriodEnum.WEEK:
        time_filter = SubscriberEarn.created_at >= now - timedelta(weeks=1)
    elif time_period == TimePeriodEnum.MONTH:
        time_filter = SubscriberEarn.created_at >= now - timedelta(weeks=4)  # Assuming a month is approximately 4 weeks
    elif time_period == TimePeriodEnum.YEAR:
        time_filter = SubscriberEarn.created_at >= now - timedelta(weeks=52)  # Assuming a year is approximately 52 weeks
    else:
        raise ValueError("Invalid time period.")

    query = base_query.where(and_(time_filter, SubscriberEarn.user_email == user_email)).order_by(SubscriberEarn.created_at)

    return query


def watch_hour_log(user_email: str, time_period: TimePeriodEnum):
    base_query = select(WatchHourEarn.watch_hour, WatchHourEarn.created_at).where(
        WatchHourEarn.user_email == user_email
    )

    now = datetime.now()
    if time_period == TimePeriodEnum.DAY:
        time_filter = WatchHourEarn.created_at >= now - timedelta(days=1)
    elif time_period == TimePeriodEnum.WEEK:
        time_filter = WatchHourEarn.created_at >= now - timedelta(weeks=1)
    elif time_period == TimePeriodEnum.MONTH:
        time_filter = WatchHourEarn.created_at >= now - timedelta(weeks=4)
    elif time_period == TimePeriodEnum.YEAR:
        time_filter = WatchHourEarn.created_at >= now - timedelta(weeks=52)
    else:
        raise ValueError("Invalid time period.")

    query = base_query.where(and_(time_filter, WatchHourEarn.user_email == user_email)).order_by(WatchHourEarn.created_at)

    return query
