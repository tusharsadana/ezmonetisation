from functools import cache

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.monetization_service.queries.users import user_exists
from src.monetization_service.schemas.api.v1.channel import ChannelIn
from src.monetization_service.queries.channel import add_channel, deselect_channels


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



@cache
def get_channel_service() -> ChannelService:
    return ChannelService()
