from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Self

from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from stores.base import NamespacedStore

if TYPE_CHECKING:
    from types import TracebackType

__all__ = ("RedisStore",)


class RedisStore(NamespacedStore):
    __slots__ = (
        "redis",
        "handle_client_shutdown",
    )

    def __init__(
            self,
            redis: Redis,
            namespace: str | None = None,
            handle_client_shutdown: bool = False
    ) -> None:
        self.redis = redis
        self.namespace = namespace
        self.handle_client_shutdown = handle_client_shutdown

    async def _shutdown(self) -> None:
        if self.handle_client_shutdown:
            await self.redis.aclose(close_connection_pool=True)

    async def __aenter__(self) -> Self:
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
            namespace: str | None = None,
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
            namespace=namespace,
        )

    def with_namespace(self, namespace: str) -> Self:
        return type(self)(
            redis=self.redis,
            namespace=f"{self.namespace}_{namespace}" if self.namespace else namespace,
            handle_client_shutdown=self.handle_client_shutdown,
        )

    def _make_key(self, key: str) -> str:
        prefix = f"{self.namespace}:" if self.namespace else ""
        return prefix + key

    async def set(self, key: str, value: str | bytes, expires_in: int | timedelta | None = None) -> None:
        if isinstance(value, str):
            value = value.encode("utf-8")
        await self.redis.set(self._make_key(key), value, ex=expires_in)

    async def get(self, key: str) -> bytes | None:
        return await self.redis.get(self._make_key(key))

    async def delete(self, key: str) -> None:
        await self.redis.delete(self._make_key(key))

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(self._make_key(key)) == 1

    async def expires_in(self, key: str) -> int | None:
        ttl = await self.redis.ttl(self._make_key(key))
        return None if ttl == -2 else ttl

    async def incr(self, key: str, amount: int = 1) -> None:
        await self.redis.incr(self._make_key(key), amount)

    async def decr(self, key: str, amount: int = 1) -> None:
        await self.redis.decr(self._make_key(key), amount)
