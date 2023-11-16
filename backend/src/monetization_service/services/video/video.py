from functools import cache
from uuid import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.monetization_service.queries.table import insert_to_table_by_model
from src.monetization_service.queries.users import user_exists, user_ratio
from src.monetization_service.schemas.api.v1.video import VideoIn, VideoSelectIn, VideoCompIn
from src.monetization_service.queries.video import (
    add_video, deselect_videos, get_video_list, video_isvalid, activate_videos, video_exists,
)
from src.monetization_service.queries.credit import user_in_watch_credit, update_watch_credit
from src.monetization_service.models.channel import WatchHourCredit, WatchHourEarn


class VideoService:

    @staticmethod
    async def add_video(session: AsyncSession, data: VideoIn):
        query = user_exists(data.user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        video_data = [{"user_email": data.user_email, "video_link": link, "is_active": False} for link in data.video_links]
        query = add_video(video_data)
        result = await session.execute(query)
        await session.commit()
        if result:
            return True, "Added videos successfully"
        else:
            return False, "Error"

    @staticmethod
    async def get_video_list(session: AsyncSession, user_email:str):
        query = user_exists(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        query = get_video_list(user_email)
        result = await session.execute(query)
        result = result.all()
        if result:
            return True, result[0][0]
        else:
            return False, "Error"

    @staticmethod
    async def activate_videos(session: AsyncSession, payload: VideoSelectIn):
        query = user_exists(payload.user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        query = video_isvalid(payload)
        result = await session.execute(query)
        result = result.all()
        if not result[0][0] == len(payload.video_ids):
            return False, "Video_ids and user_email do not match"
        query = deselect_videos(payload.user_email)
        await session.execute(query)
        query = activate_videos(payload.video_ids)
        result = await session.execute(query)
        await session.commit()
        if result:
            return True, "Videos activated successfully"
        else:
            return False, "Error"

    @staticmethod
    async def complete_video(session: AsyncSession, payload: VideoCompIn):
        user_w = payload.user_email
        query = user_exists(user_w)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        query = video_exists(payload.video_id)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid video_id"
        user_v = result[0]

        query = user_ratio(user_v)
        result = await session.execute(query)
        user_v_ratio = result.one_or_none()

        query = user_ratio(user_w)
        result = await session.execute(query)
        user_w_ratio = result.one_or_none()

        user_v_credit = -1*payload.video_duration*user_v_ratio[0]
        user_w_credit = payload.video_duration*user_w_ratio[0]

        query = user_in_watch_credit(user_v)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            insert_query = insert_to_table_by_model(
                WatchHourCredit, {"user_email": user_v, "watch_hour": user_v_credit}
            )
            await session.execute(insert_query)
        else:
            query = update_watch_credit(user_v, user_v_credit)
            await session.execute(query)

        insert_query = insert_to_table_by_model(
                WatchHourEarn, {"user_email": user_v, "watch_hour": user_v_credit}
            )
        await session.execute(insert_query)

        query = user_in_watch_credit(user_w)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            insert_query = insert_to_table_by_model(
                WatchHourCredit, {"user_email": user_w, "watch_hour": user_w_credit}
            )
            await session.execute(insert_query)
        else:
            query = update_watch_credit(user_w, user_w_credit)
            await session.execute(query)
        insert_query = insert_to_table_by_model(
                WatchHourEarn, {"user_email": user_w, "watch_hour": user_w_credit}
            )
        await session.execute(insert_query)
        await session.commit()

        return True, "Video completed successfully"


@cache
def get_video_service() -> VideoService:
    return VideoService()
