# thirdparty
from sqlalchemy import Boolean, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType

# project
from src.monetization_service.core.db import Base
from src.monetization_service.models.mixins import TimeMixin, IdMixin


class User(TimeMixin, Base):
    """Table for storing users info"""

    __tablename__ = "user"

    email = Column(
        String,
        comment="Email of user",
        nullable=False,
        default=False,
        primary_key=True,
        unique=True,
    )
    first_name = Column(
        String,
        comment="First Name of user",
        nullable=True,
    )
    last_name = Column(
        String,
        comment="Last Name of user",
        nullable=True,
    )

    user_type_constants = relationship("UserTypeConstants", back_populates="user")
    user_type = Column(
        Integer,
        ForeignKey("user_type_constants.user_type_id"),
        comment="User Type",
        nullable=False,
        default=1
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Is this user active or not",
    )

    password = Column(
        PasswordType(
            schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]
        ),
        nullable=True,
    )
    channel = relationship("Channel")
    video = relationship("Video")
    watch_hour_earn = relationship("WatchHourEarn")
    subscriber_earn = relationship("SubscriberEarn")
    watch_hour_credit = relationship("WatchHourCredit")
    subscriber_credit = relationship("SubscriberCredit")


class UserTypeConstants(IdMixin, TimeMixin, Base):
    """Table for storing user type constants"""

    __tablename__ = "user_type_constants"

    user_type_id = Column(
        Integer,
        comment="User Type ID",
        nullable=False,
        unique=True,
    )
    user_type_name = Column(
        String,
        comment="User Type name",
        nullable=True,
    )
    watch_hour_ratio = Column(
        Float,
        comment="Watch Hour Ratio",
        nullable=False,
        default=1
    )
    subscriber_ratio = Column(
        Float,
        comment="Subscriber Ratio",
        nullable=False,
        default=1
    )
    user = relationship("User")
