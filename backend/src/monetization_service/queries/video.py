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

from src.monetization_service.schemas.api.v1.video import VideoIn, VideoSelectIn
from src.monetization_service.models.channel import Video


def add_video(video_data: list[dict]) -> Insert:
    query = (
        insert(Video)
        .values(
            video_data
        )
        .returning(Video.id)
    )

    return query


def deselect_videos(user_email: str):
    query = (
        update(Video)
        .where(Video.user_email == user_email)
        .values(is_active=False)
    )
    return query


def activate_videos(video_ids: list[UUID]):
    query = (
        update(Video)
        .where(Video.id.in_(video_ids))
        .values(is_active=True)
    )
    return query


def get_video_list(user_email: str):
    query = (
        select(
            func.json_agg(
                func.json_build_object(
                    'id', Video.id,
                    'video_link', Video.video_link,
                    'is_active', Video.is_active
                )
            ).label('channels')
        )
        .filter(Video.user_email == user_email)
        .group_by(Video.user_email)
    )
    return query


def video_isvalid(data: VideoSelectIn):
    query = (
        select(func.count())
        .where(and_(Video.id.in_(data.video_ids), Video.user_email == data.user_email))
    )
    return query


def video_exists(video_id: UUID):
    query = (
        select(Video.user_email)
        .where(Video.id == video_id)
    )
    return query



