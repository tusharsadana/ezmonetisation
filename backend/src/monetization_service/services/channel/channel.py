from functools import cache
from uuid import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.monetization_service.queries.users import user_exists
from src.monetization_service.schemas.api.v1.channel import ChannelIn
from src.monetization_service.queries.channel import (
    add_channel, deselect_channels, get_channel_list, channel_isvalid, select_channel
)


class ChannelService:

    @staticmethod
    async def add_channel(session: AsyncSession, data: ChannelIn):
        query = user_exists(data.username)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid username"
        query = deselect_channels(data.username)
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
    async def get_channel_list(session: AsyncSession, username:str):
        query = user_exists(username)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid username"
        query = get_channel_list(username)
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


@cache
def get_channel_service() -> ChannelService:
    return ChannelService()
