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
    and_,
)
from sqlalchemy.sql import nullslast
from sqlalchemy.sql.functions import count, func

from src.monetization_service.schemas.api.v1.channel import ChannelIn
from src.monetization_service.models.channel import Channel, SubscriberEarn, SubscriberCredit
from src.monetization_service.models.user import User


def add_channel(channel_data: ChannelIn) -> Insert:
    query = (
        insert(Channel)
        .values(
            user_email=channel_data.user_email,
            channel_name=channel_data.channel_name,
            channel_link=channel_data.channel_link,
            is_selected=True
        )
        .returning(Channel.id)
    )

    return query


def deselect_channels(user_email: str):
    query = (
        update(Channel)
        .where(Channel.user_email == user_email)
        .values(is_selected=False)
    )
    return query


def select_channel(channel_id: UUID):
    query = (
        update(Channel)
        .where(Channel.id == channel_id)
        .values(is_selected=True)
    )
    return query


def get_channel_list(user_email: str):
    query = (
        select(
            func.json_agg(
                func.json_build_object(
                    'id', Channel.id,
                    'channel_name', Channel.channel_name,
                    'channel_link', Channel.channel_link,
                    'is_selected', Channel.is_selected
                )
            ).label('channels')
        )
        .filter(Channel.user_email == user_email)
        .group_by(Channel.user_email)
    )
    return query


def channel_isvalid(channel_id: UUID):
    query = (
        select(Channel.user_email)
        .where(Channel.id == channel_id)
    )
    return query


def channel_exists(channel_id: UUID):
    query = (
        select(Channel.user_email)
        .where(and_(Channel.id == channel_id, Channel.is_selected))
    )
    return query


def fetch_channels(user_email: str, num: int):
    subquery = (
        select(SubscriberCredit.user_email)
        .join(User, User.email == SubscriberCredit.user_email)
        .filter(and_(SubscriberCredit.subscriber_earn > 0.5, User.is_active, SubscriberCredit.user_email != user_email))
        .subquery("subquery")
    )

    users = (
        select(SubscriberEarn.user_email, func.max(SubscriberEarn.created_at))
        .join(subquery, SubscriberEarn.user_email == subquery.c.user_email)
        .filter(SubscriberEarn.subscriber_earn > 0)
        .group_by(SubscriberEarn.user_email)
        .order_by(func.min(SubscriberEarn.created_at))
        .limit(num)
    ).subquery("users")

    random_records = (
        select(Channel.id, Channel.channel_link, Channel.user_email)
        .join(users, Channel.user_email == users.c.user_email)
        .filter(Channel.is_selected)
        .order_by(func.random())
    )
    return random_records
