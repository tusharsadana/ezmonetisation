# stdlib
from functools import cache

# thirdparty
from redis.asyncio import Redis

# project
from src.monetization_service.settings.development import settings


@cache
def get_redis_client() -> Redis:
    client = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True,
    )

    return client
