from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from redis.exceptions import RedisError

from core.logger import logger


async def init_cache(
        redis_url: str,
        prefix: str = "",
        expire: int = 60
) -> None:
    try:
        redis = Redis.from_url(url=redis_url)
        await redis.ping()
        FastAPICache.init(RedisBackend(redis=redis), prefix=prefix, expire=expire)
        return
    except RedisError as ex:
        logger.error(f"Failed to init Redis cache: {ex}")
