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
from sqlalchemy.sql import nullslast
from sqlalchemy.sql.functions import count, func

from src.monetization_service.schemas.api.v1.channel import ChannelIn
from src.monetization_service.models.channel import Channel


def add_channel(channel_data: ChannelIn) -> Insert:
    query = (
        insert(Channel)
        .values(
            user_email=channel_data.username,
            channel_name=channel_data.channel_name,
            channel_link=channel_data.channel_link,
            is_selected=True
        )
        .returning(Channel.id)
    )

    return query


def deselect_channels(username: str):
    query = (
        update(Channel)
        .where(Channel.user_email == username)
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


def get_channel_list(username: str):
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
        .filter(Channel.user_email == username)
        .group_by(Channel.user_email)
    )
    return query


def channel_isvalid(channel_id: UUID):
    query = (
        select(Channel.user_email)
        .where(Channel.id == channel_id)
    )
    return query
