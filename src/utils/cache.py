from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

from dependency_injector.wiring import inject, Provide
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.exceptions import RedisError

from core.container import ServiceContainer

if TYPE_CHECKING:
    from redis.asyncio import Redis

logger = logging.getLogger("hotel_booking")


@inject
async def init_cache(
        redis: Redis = Provide[ServiceContainer.redis],
        prefix: str = "",
        expire: int = 60
) -> None:
    try:
        await redis.ping()
        FastAPICache.init(RedisBackend(redis=redis), prefix=prefix, expire=expire)
    except RedisError as ex:
        logger.exception(f"Failed to init Redis cache: {ex}")
        sys.exit(1)
