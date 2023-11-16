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
from src.monetization_service.models.channel import WatchHourCredit


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
