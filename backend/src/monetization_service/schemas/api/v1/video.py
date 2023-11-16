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


class VideoIn(BaseModel):
    user_email: constr(strip_whitespace=True, min_length=1)
    video_links: List[constr(strip_whitespace=True, min_length=1)]

    @validator("video_links")
    def validate_video_links(cls, value):
        video_link_pattern = re.compile(r'https://www\.youtube\.com/watch\?v=[a-zA-Z0-9_-]+')

        for link in value:
            if not video_link_pattern.fullmatch(link):
                raise ValueError("Invalid video link format")

        return value

    class Config:
        orm_mode = True


class VideoSelectIn(BaseModel):
    user_email: constr(strip_whitespace=True, min_length=1)
    video_ids: List[UUID]

    class Config:
        orm_mode = True


class VideoCompIn(BaseModel):
    user_email: constr(strip_whitespace=True, min_length=1)
    video_id: UUID
    video_duration: float

    class Config:
        orm_mode = True
