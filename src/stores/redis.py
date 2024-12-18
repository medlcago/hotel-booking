from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from .base import Store

if TYPE_CHECKING:
    from types import TracebackType

__all__ = ("RedisStore",)


class RedisStore(Store):
    __slots__ = (
        "redis",
        "handle_client_shutdown",
    )

    def __init__(
            self,
            redis: Redis,
            handle_client_shutdown: bool = False
    ) -> None:
        self.redis = redis
        self.handle_client_shutdown = handle_client_shutdown

    async def _shutdown(self) -> None:
        if self.handle_client_shutdown:
            await self.redis.aclose(close_connection_pool=True)

    async def __aenter__(self) -> RedisStore:
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        await self._shutdown()

    @classmethod
    def with_client(
            cls,
            url: str = "redis://localhost:6379",
            *,
            db: int | None = None,
            port: int | None = None,
            username: str | None = None,
            password: str | None = None,
    ) -> RedisStore:
        pool: ConnectionPool = ConnectionPool.from_url(
            url=url,
            db=db,
            decode_responses=False,
            port=port,
            username=username,
            password=password,
        )
        return cls(
            redis=Redis(connection_pool=pool),
            handle_client_shutdown=True,
        )

    async def set(self, key: str, value: str | bytes, expires_in: int | timedelta | None = None) -> None:
        if isinstance(value, str):
            value = value.encode("utf-8")
        await self.redis.set(key, value, ex=expires_in)

    async def get(self, key: str) -> bytes | None:
        return await self.redis.get(key)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key) == 1

    async def expires_in(self, key: str) -> int | None:
        ttl = await self.redis.ttl(key)
        return None if ttl == -2 else ttl
