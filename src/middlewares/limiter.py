import logging
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi.requests import Request

from core.container import Container
from core.exceptions import TooManyRequestsException
from stores.base import NamespacedStore
from utils.ip_address import extract_ip_address

logger = logging.getLogger("hotel_booking")


class BaseRateLimiter(ABC):
    async def __call__(self, request: Request) -> Any:
        key = self.make_key(request)
        return await self.dispatch(key)

    @staticmethod
    def make_key(request: Request) -> str:
        user_ip = extract_ip_address(request)
        user_agent = request.headers.get("User-Agent")
        logger.info(f"user_ip: {user_ip}, user_agent: {user_agent}")
        return f"{user_ip}:{user_agent}"

    def raise_exception(self, retry_after: int) -> None:
        raise TooManyRequestsException(headers={"Retry-After": str(retry_after)})

    @abstractmethod
    async def dispatch(self, key: str) -> Any:
        raise NotImplementedError


class RateLimiter(BaseRateLimiter):
    def __init__(
            self,
            store: NamespacedStore,
            *,
            limit: int,
            ttl: int | timedelta
    ):
        self.store = store
        self.limit = limit
        self.ttl = ttl

    async def dispatch(self, key: str) -> Any:
        value = await self.store.get(key)
        if not value:
            await self.store.set(key, "1", expires_in=self.ttl)
            return
        value = int(value.decode("utf-8"))
        if value >= self.limit:
            expires_in = await self.store.expires_in(key)
            self.raise_exception(expires_in)
        else:
            await self.store.incr(key)


@inject
def Limiter(
        store: NamespacedStore = Provide[Container.redis_store],
        *,
        limit: int,
        ttl: int | timedelta
):
    rl = RateLimiter(
        store=store.with_namespace("rate_limit"),
        limit=limit,
        ttl=ttl
    )

    async def wrapper(request: Request) -> Any:
        return await rl(request)

    return wrapper
