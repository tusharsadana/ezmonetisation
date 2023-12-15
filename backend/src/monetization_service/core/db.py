# stdlib
import logging
from asyncio import current_task
from contextlib import asynccontextmanager

# thirdparty
import sqlalchemy
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

# project
from src.monetization_service.settings.development import settings

logger = logging.getLogger("PG_CONNECTIONS")

SQLALCHEMY_URL = URL.create(
    drivername="postgresql+asyncpg",
    host=settings.db.host,
    username=settings.db.user,
    password=settings.db.password,
    port=settings.db.port,
    database=settings.db.db,
)

if settings.db.connection_number:
    POOL_SIZE = settings.db.connection_number
else:
    POOL_SIZE = max(
        int((settings.db.max_connections / settings.uvicorn.workers) - 1), 1
    )

engine = create_async_engine(
    SQLALCHEMY_URL, pool_size=POOL_SIZE, max_overflow=0
)

async_session_maker = async_scoped_session(
    async_sessionmaker(bind=engine), scopefunc=current_task
)

Base = declarative_base()


async def get_session():
    session = async_session_maker()
    # yield session
    try:
        yield session
    finally:
        result = await session.execute(
            sqlalchemy.text("SELECT sum(numbackends) FROM pg_stat_database;")
        )
        logger.info(f"Current connections: {result.one()[0]}/{POOL_SIZE}")
        await session.close()


@asynccontextmanager
async def get_session_cm():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()
