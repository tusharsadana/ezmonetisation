import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

# thirdparty
from pydantic.types import constr
from pydantic import validator
import re
from sqlalchemy import UnaryExpression, asc, desc

# project
from src.common.schemas.base import BaseModel


class ChannelIn(BaseModel):
    user_email: constr(strip_whitespace=True, min_length=1)
    channel_name: constr(strip_whitespace=True, min_length=1)
    channel_link: constr(
        strip_whitespace=True, min_length=1,)

    @validator("channel_link")
    def validate_channel_link(cls, value):
        format1_pattern = re.compile(r'https://www\.youtube\.com/channel/[a-zA-Z0-9_-]+')
        format2_pattern = re.compile(r'https://www\.youtube\.com/@[a-zA-Z0-9_-]+')
        format3_pattern = re.compile(r'https://www\.youtube\.com/[a-zA-Z0-9_-]+')

        if not (format1_pattern.match(value) or format2_pattern.match(value) or format3_pattern.match(value)):
            raise ValueError("Invalid channel link format")

        return value

    class Config:
        orm_mode = True


class ChannelSubIn(BaseModel):
    user_email: constr(strip_whitespace=True, min_length=1)
    channel_id: UUID

    class Config:
        orm_mode = True

