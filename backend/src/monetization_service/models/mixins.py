# stdlib
import uuid

# thirdparty
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr


class IdMixin:
    @declared_attr
    def id(cls):
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            comment="ID",
            default=uuid.uuid4,
        )


class TimeMixin:
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime,
            server_default=func.now(),
            nullable=False,
            comment="Creation date",
        )

    @declared_attr
    def modified_at(cls):
        return Column(
            DateTime,
            server_default=func.now(),
            nullable=False,
            comment="Modified date",
        )
