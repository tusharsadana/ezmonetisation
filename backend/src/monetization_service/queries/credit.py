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

from sqlalchemy.sql.functions import count, func
from src.monetization_service.models.channel import WatchHourCredit, SubscriberCredit, SubscriberEarn, WatchHourEarn


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


def subscriber_log(user_email: str, start_date: date, end_date: date, scale: str):

    subscriber_cte = (
        select(SubscriberEarn)
        .filter(SubscriberEarn.user_email == user_email)
        .cte("subscriber_cte")
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
                "subscribers",
                func.coalesce(func.sum(subscriber_cte.c.subscriber_earn), 0),
            ),
        )
        .outerjoin(
            subscriber_cte,
            func.date_trunc(scale, subscriber_cte.c.created_at)
            == func.date_trunc(scale, date_cte.c.date),
        )
        .group_by(scale, date_cte.c.date)
        .order_by(scale, date_cte.c.date)
    )

    return q


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

