from __future__ import annotations

import logging
import sys

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from redis.exceptions import RedisError

logger = logging.getLogger("hotel_booking")


async def init_cache(
        redis_url: str,
        prefix: str = "",
        expire: int = 60
) -> None:
    try:
        redis = Redis.from_url(redis_url)
        await redis.ping()
        FastAPICache.init(RedisBackend(redis=redis), prefix=prefix, expire=expire)
    except RedisError as ex:
        logger.exception(f"Failed to init Redis cache: {ex}")
        sys.exit(1)
