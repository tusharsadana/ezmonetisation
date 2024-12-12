from functools import cache
from sqlalchemy.ext.asyncio import AsyncSession
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io


from src.monetization_service.queries.credit import (
    user_in_sub_credit, subscriber_log, user_in_watch_credit, watch_hour_log
)
from src.monetization_service.queries.users import user_exists
from src.monetization_service.schemas.api.v1.dashboard import DateFilter


class DashboardService:

    @staticmethod
    async def subscriber_earn_graph(session: AsyncSession, user_email: str, date_filter: DateFilter):
        query = user_exists(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        scale = date_filter.scale.value
        query = subscriber_log(user_email, date_filter.start_date, date_filter.end_date, scale)
        result = await session.execute(query)
        data = result.all()
        result = [{'x': item[0], 'y': item[1]} for item in data]
        return True, result

    @staticmethod
    async def watch_hour_earn_graph(session: AsyncSession, user_email: str, date_filter: DateFilter):
        query = user_exists(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        scale = date_filter.scale.value
        query = watch_hour_log(user_email, date_filter.start_date, date_filter.end_date, scale)
        result = await session.execute(query)
        data = result.all()
        result = [{'x': item[0], 'y': item[1]} for item in data]
        return True, result


@cache
def get_dashboard_service() -> DashboardService:
    return DashboardService()
