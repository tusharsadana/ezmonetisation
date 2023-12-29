from enum import Enum
from src.common.schemas.base import BaseModel
from datetime import date, timedelta
from pydantic import Field


class TimePeriodEnum(str, Enum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class FrequencySelector(str, Enum):

    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class DateFilter(BaseModel):

    start_date: date | None = Field(
        default=date.today() - timedelta(days=7)
    )
    end_date: date | None = Field(default=date.today())
    scale: FrequencySelector | None = Field(default=FrequencySelector.DAY)

