from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from redis.exceptions import RedisError

from core.logger import logger


async def init_cache(
        redis_url: str | None = None,
        prefix: str = "",
        expire: int = 60
) -> None:
    if redis_url:
        try:
            redis = Redis.from_url(url=redis_url)
            await redis.ping()
            FastAPICache.init(RedisBackend(redis=redis), prefix=prefix, expire=expire)
            logger.info("Using redis cache")
            return
        except RedisError as ex:
            logger.error(ex)
    FastAPICache.init(InMemoryBackend(), prefix=prefix, expire=expire)
    logger.info("Using in-memory cache")
