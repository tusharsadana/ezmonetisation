# stdlib
from typing import Any, Type

# thirdparty
from sqlalchemy import insert
from sqlalchemy.sql.expression import Insert

from src.monetization_service.core.db import Base


def insert_to_table_by_model(
    orm_model: Type[Base], data: dict[str, Any] | list[dict[str, Any]]
) -> Insert | list[Insert]:
    """Insert data to custom table by ORM model"""
    query = insert(orm_model).values(data)
    return query
