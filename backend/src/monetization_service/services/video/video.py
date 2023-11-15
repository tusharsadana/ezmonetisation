from functools import cache
from uuid import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.monetization_service.queries.users import user_exists
from src.monetization_service.schemas.api.v1.video import VideoIn, VideoSelectIn
from src.monetization_service.queries.video import (
    add_video, deselect_videos, get_video_list, video_isvalid, activate_videos
)


class VideoService:

    @staticmethod
    async def add_video(session: AsyncSession, data: VideoIn):
        query = user_exists(data.username)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid username"
        video_data = [{"user_email": data.username, "video_link": link, "is_active": False} for link in data.video_links]
        query = add_video(video_data)
        result = await session.execute(query)
        await session.commit()
        if result:
            return True, "Added videos successfully"
        else:
            return False, "Error"

    @staticmethod
    async def get_video_list(session: AsyncSession, username:str):
        query = user_exists(username)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid username"
        query = get_video_list(username)
        result = await session.execute(query)
        result = result.all()
        if result:
            return True, result[0][0]
        else:
            return False, "Error"

    @staticmethod
    async def activate_videos(session: AsyncSession, payload: VideoSelectIn):
        query = user_exists(payload.username)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid username"
        query = video_isvalid(payload)
        result = await session.execute(query)
        result = result.all()
        if not result[0][0] == len(payload.video_ids):
            return False, "Video_ids and username do not match"
        query = deselect_videos(payload.username)
        await session.execute(query)
        query = activate_videos(payload.video_ids)
        result = await session.execute(query)
        await session.commit()
        if result:
            return True, "Videos activated successfully"
        else:
            return False, "Error"


@cache
def get_video_service() -> VideoService:
    return VideoService()
