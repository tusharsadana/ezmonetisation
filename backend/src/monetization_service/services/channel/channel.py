from functools import cache
from uuid import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.monetization_service.models.channel import SubscriberCredit, SubscriberEarn
from src.monetization_service.queries.credit import user_in_sub_credit, update_sub_credit
from src.monetization_service.queries.table import insert_to_table_by_model
from src.monetization_service.queries.users import user_exists, user_ratio, user_num_limit
from src.monetization_service.schemas.api.v1.channel import ChannelIn, ChannelSubIn
from src.monetization_service.queries.channel import (
    add_channel, deselect_channels, get_channel_list, channel_isvalid, select_channel, channel_exists, fetch_channels
)


class ChannelService:

    @staticmethod
    async def add_channel(session: AsyncSession, data: ChannelIn):
        query = user_exists(data.user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        query = user_in_sub_credit(data.user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            insert_query = insert_to_table_by_model(
                SubscriberCredit, {"user_email": data.user_email, "subscriber_earn": 2}
            )
            await session.execute(insert_query)
        query = deselect_channels(data.user_email)
        await session.execute(query)
        query = add_channel(data)
        result = await session.execute(query)
        await session.commit()
        result = result.one_or_none()
        if result:
            return True, "Added channel successfully"
        else:
            return False, "Error"

    @staticmethod
    async def get_channel_list(session: AsyncSession, user_email: str):
        query = user_exists(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        query = get_channel_list(user_email)
        result = await session.execute(query)
        result = result.all()
        if result:
            return True, result[0][0]
        else:
            return False, "Error"

    @staticmethod
    async def select_channel(session: AsyncSession, channel_id: UUID):
        query = channel_isvalid(channel_id)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid channel_id"
        result = result[0]
        query = deselect_channels(result)
        await session.execute(query)
        query = select_channel(channel_id)
        result = await session.execute(query)
        await session.commit()
        if result:
            return True, "Channel selected successfully"
        else:
            return False, "Error"

    @staticmethod
    async def subscribe_channel(session: AsyncSession, payload: ChannelSubIn):
        user_prd = payload.user_email
        query = user_exists(user_prd)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        query = channel_exists(payload.channel_id)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid channel_id"
        user_csmr = result[0]
        if user_csmr == user_prd:
            return False, "Cannot subscribe to your own channel"

        query = user_ratio(user_prd)
        result = await session.execute(query)
        user_csmr_ratio = result.one_or_none()
        user_csmr_credit = -1
        user_prd_credit = user_csmr_ratio[1]

        query = user_in_sub_credit(user_csmr)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            insert_query = insert_to_table_by_model(
                SubscriberCredit, {"user_email": user_csmr, "subscriber_earn": user_csmr_credit}
            )
            await session.execute(insert_query)
        else:
            query = update_sub_credit(user_csmr, user_csmr_credit)
            await session.execute(query)

        insert_query = insert_to_table_by_model(
                SubscriberEarn, {"user_email": user_csmr, "subscriber_earn": user_csmr_credit}
            )
        await session.execute(insert_query)

        query = user_in_sub_credit(user_prd)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            insert_query = insert_to_table_by_model(
                SubscriberCredit, {"user_email": user_prd, "subscriber_earn": user_prd_credit}
            )
            await session.execute(insert_query)
        else:
            query = update_sub_credit(user_prd, user_prd_credit)
            await session.execute(query)
        insert_query = insert_to_table_by_model(
                SubscriberEarn, {"user_email": user_prd, "subscriber_earn": user_prd_credit}
            )
        await session.execute(insert_query)
        await session.commit()

        return True, "Subscribed successfully"

    @staticmethod
    async def fetch_channels(session: AsyncSession, user_email: str, num: int):
        query = user_exists(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"

        query = user_num_limit(user_email)
        result = await session.execute(query)
        sub_num_limit = result.one_or_none()
        if sub_num_limit[1] < num:
            return False, f"Number of channels to be fetched cannot be more than {sub_num_limit[1]}"

        query = fetch_channels(user_email, num)
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
        data = [{"channel_id": str(uid), "channel_link": link} for uid, link, email in result_list]
        return True, data


@cache
def get_channel_service() -> ChannelService:
    return ChannelService()
