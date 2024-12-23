import logging
from abc import ABC, abstractmethod
from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi.requests import Request

from core.container import Container
from core.exceptions import TooManyRequestsException
from stores.base import NamespacedStore

logger = logging.getLogger("hotel_booking")


class ThrottlingMiddlewareBase(ABC):
    async def __call__(self, request: Request) -> Any:
        key = self.make_key(request)
        return await self.throttle(key)

    @staticmethod
    def make_key(request: Request) -> str:
        user_ip = (
                request.headers.get("X-Forwarded-For") or
                request.headers.get("X-Real-Ip") or
                request.headers.get("REMOTE_ADDR") or
                request.client.host
        )
        user_agent = request.headers.get("User-Agent")
        logger.info(f"user_ip: {user_ip}, user_agent: {user_agent}")
        return f"{user_ip}:{user_agent}"

    def raise_exception(self) -> None:
        raise TooManyRequestsException

    @abstractmethod
    async def throttle(self, key: str) -> Any:
        raise NotImplementedError


class ThrottlingMiddleware(ThrottlingMiddlewareBase):
    def __init__(
            self,
            store: NamespacedStore,
            *,
            limit: int,
            throttle_time: int
    ):
        self.store = store
        self.limit = limit
        self.throttle_time = throttle_time

    async def throttle(self, key: str) -> Any:
        value = await self.store.get(key)
        if value:
            value = int(value.decode("utf-8"))
            if value >= self.limit:
                self.raise_exception()
            else:
                await self.store.incr(key)
        else:
            await self.store.set(key, "1", expires_in=self.throttle_time)


@inject
def Throttling(
        store: NamespacedStore = Provide[Container.redis_store],
        *,
        limit: int,
        throttle_time: int
):
    tm = ThrottlingMiddleware(
        store=store.with_namespace("throttling"),
        limit=limit,
        throttle_time=throttle_time
    )

    async def wrapper(request: Request) -> Any:
        return await tm(request)

    return wrapper
