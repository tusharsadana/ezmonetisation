from functools import cache
from uuid import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.monetization_service.queries.table import insert_to_table_by_model
from src.monetization_service.queries.users import user_exists, user_ratio, user_num_limit, user_watch_privileges
from src.monetization_service.schemas.api.v1.video import VideoIn, VideoSelectIn, VideoCompIn
from src.monetization_service.queries.video import (
    add_video, deselect_videos, get_video_list, video_isvalid, activate_videos, video_exists, fetch_videos
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
        query = user_in_watch_credit(data.user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            insert_query = insert_to_table_by_model(
                WatchHourCredit, {"user_email": data.user_email, "watch_hour": 2}
            )
            await session.execute(insert_query)
            insert_query = insert_to_table_by_model(
                WatchHourEarn, {"user_email": data.user_email, "watch_hour": 2}
            )
            await session.execute(insert_query)

        video_data = [{"user_email": data.user_email, "video_link": link, "is_active": False} for link in data.video_links]
        query = add_video(video_data)
        result = await session.execute(query)
        await session.commit()
        if result:
            return True, "Added videos successfully"
        else:
            return False, "Error"

    @staticmethod
    async def get_video_list(session: AsyncSession, user_email: str):
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
        query = user_watch_privileges(payload.user_email)
        result = await session.execute(query)
        result = result.all()
        data = result[0][0][0]
        if len(payload.video_ids) > data['Maximum videos allowed']:
            return False, f"No more than {data['Maximum videos allowed']} videos can be active at a time"
        if len(payload.video_ids) < data['Minimum videos allowed']:
            return False, f"Please activate at least {data['Minimum videos allowed']} videos"
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
        if user_v == user_w:
            return False, "Cannot watch your own video"

        query = user_ratio(user_w)
        result = await session.execute(query)
        user_w_ratio = result.one_or_none()

        user_v_credit = -1*payload.video_duration
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

    @staticmethod
    async def fetch_videos(session: AsyncSession, user_email: str, num: int):
        query = user_exists(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"

        query = user_num_limit(user_email)
        result = await session.execute(query)
        vid_num_limit = result.one_or_none()
        if vid_num_limit[0] < num:
            return False, f"Number of videos to be fetched cannot be more than {vid_num_limit[0]}"

        query = fetch_videos(user_email, num)
        result = await session.execute(query)
        result = result.all()
        result_dict = {}
        counter = 0
        for item in result:
            uuid, url, email = item
            if email not in result_dict:
                result_dict[email] = item
                counter += 1
                if counter == num:
                    break
        result_list = list(result_dict.values())
        data = [{"video_id": str(uid), "video_link": link} for uid, link, email in result_list]
        return True, data

    @staticmethod
    async def user_watch_privileges(session: AsyncSession, user_email: str):
        query = user_exists(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        query = user_watch_privileges(user_email)
        result = await session.execute(query)
        result = result.all()
        return True, result[0][0][0]

@cache
def get_video_service() -> VideoService:
    return VideoService()
