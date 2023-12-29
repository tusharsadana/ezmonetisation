from uuid import UUID
from datetime import date

# thirdparty
from sqlalchemy import (
    literal,
    select,
    update,
    text,
    label,
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


def watch_hour_log(user_email: str, start_date: date, end_date: date, scale: str):
    watch_hour_cte = (
        select(WatchHourEarn)
        .filter(WatchHourEarn.user_email == user_email)
        .cte("watch_hour_cte")
    )

    date_cte = select(
        func.generate_series(
            func.date_trunc(scale, literal(start_date)),
            func.date_trunc(scale, literal(end_date)),
            text(f"'1 {scale}'::interval"),
        ).label("date")
    ).cte("date_cte")

    q = (
        select(
            func.date_trunc(scale, date_cte.c.date).label(scale),
            label(
                "watch_hours",
                func.coalesce(func.sum(watch_hour_cte.c.watch_hour), 0),
            ),
        )
        .outerjoin(
            watch_hour_cte,
            func.date_trunc(scale, watch_hour_cte.c.created_at)
            == func.date_trunc(scale, date_cte.c.date),
        )
        .group_by(scale, date_cte.c.date)
        .order_by(scale, date_cte.c.date)
    )

    return q

