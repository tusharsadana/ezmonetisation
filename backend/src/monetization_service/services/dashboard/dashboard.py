from functools import cache
from sqlalchemy.ext.asyncio import AsyncSession
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io


from src.monetization_service.queries.credit import (
    user_in_sub_credit, subscriber_log, user_in_watch_credit, watch_hour_log
)
from src.monetization_service.queries.users import user_exists
from src.monetization_service.schemas.api.v1.dashboard import TimePeriodEnum, DateFilter


class DashboardService:

    @staticmethod
    async def subscriber_earn_graph(session: AsyncSession, user_email: str, time_period: TimePeriodEnum):
        query = user_exists(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "Invalid user_email"
        query = user_in_sub_credit(user_email)
        result = await session.execute(query)
        result = result.one_or_none()
        if not result:
            return False, "User is yet to earn and consume any subscribers"
        query = subscriber_log(user_email, time_period)
        result = await session.execute(query)
        data = result.all()
        if not len(data):
            return False, "No user activity in the given time period"

        c_pos = 0
        c_neg = 0
        positive_values = list()
        negative_values = list()
        for x, y in data:
            if x > 0:
                positive_values.append((y, c_pos+x))
                c_pos = c_pos + x
            else:
                negative_values.append((y, c_neg+abs(x)))
                c_neg = c_neg + abs(x)

        if len(positive_values) and len(negative_values):
            if positive_values[-1][0] > negative_values[-1][0]:
                negative_values.append((positive_values[-1][0], c_neg))
            elif positive_values[-1][0] < negative_values[-1][0]:
                positive_values.append((negative_values[-1][0], c_pos))

        if len(positive_values):
            positive_x, positive_y = zip(*positive_values)
        if len(negative_values):
            negative_x, negative_y = zip(*negative_values)

        plt.figure(figsize=(12, 7))

        if len(positive_values):
            plt.plot_date(positive_x, positive_y, '-o', label='Subscribers Earned')
        if len(negative_values):
            plt.plot_date(negative_x, negative_y, '-o', label='Subscribers Consumed')

        plt.xlabel('Time')
        plt.ylabel('Subscribers')
        plt.title('Cumulative Subscribers')
        plt.legend()
        plt.grid(True)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M %d-%m'))
        plt.gcf().autofmt_xdate()

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)

        plt.close()

        return True, img_buf

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
