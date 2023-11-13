# thirdparty
from sqlalchemy import Boolean, Column, ForeignKey, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

# project
from src.monetization_service.core.db import Base
from src.monetization_service.models.mixins import TimeMixin, IdMixin


class Channel(IdMixin, TimeMixin, Base):
    """Table for storing channel links of users"""

    __tablename__ = "channel"

    user = relationship("User", back_populates="channel")
    user_email = Column(
        String,
        ForeignKey("user.email"),
        comment="User email of the linked channel",
        nullable=False,
    )

    channel_name = Column(String, nullable=False, comment="Channel name")
    channel_link = Column(String, nullable=False, comment="Channel link")
    is_selected = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Channel is selected or not",
    )


class Video(IdMixin, TimeMixin, Base):
    """Table for storing channel links of users"""

    __tablename__ = "video"

    user = relationship("User", back_populates="video")
    user_email = Column(
        String,
        ForeignKey("user.email"),
        comment="User email of the linked video",
        nullable=False,
    )
    video_link = Column(String, nullable=False, comment="Video link")
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Video is activated or not",
    )


class WatchHourEarn(IdMixin, TimeMixin, Base):
    """Table for storing channel links of users"""

    __tablename__ = "watch_hour_earn"

    user = relationship("User", back_populates="watch_hour_earn")
    user_email = Column(
        String,
        ForeignKey("user.email"),
        comment="User email of the linked channel",
        nullable=False,
    )
    watch_hour = Column(Float, nullable=False, comment="Watch hour")


class SubscriberEarn(IdMixin, TimeMixin, Base):
    """Table for storing channel links of users"""

    __tablename__ = "subscriber_earn"

    user = relationship("User", back_populates="subscriber_earn")
    user_email = Column(
        String,
        ForeignKey("user.email"),
        comment="User email of the linked channel",
        nullable=False,
    )
    subscriber_earn = Column(Integer, nullable=False, comment="Subscriber earn")



