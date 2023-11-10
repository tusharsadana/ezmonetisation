# thirdparty
from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType

# project
from src.monetization_service.core.db import Base
from src.monetization_service.models.mixins import TimeMixin


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

    user_type = Column(
        Integer, comment="User Type", nullable=False, default="1"
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


