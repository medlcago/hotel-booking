from abc import ABC, abstractmethod
from datetime import timedelta
from types import TracebackType
from typing import Self


class Store(ABC):
    __slots__ = ()

    @abstractmethod
    async def set(self, key: str, value: str | bytes, expires_in: int | timedelta | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> bytes | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def expires_in(self, key: str) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def incr(self, key: str, amount: int = 1) -> None:
        raise NotImplementedError

    @abstractmethod
    async def decr(self, key: str, amount: int = 1) -> None:
        raise NotImplementedError

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        pass


class NamespacedStore(Store):
    __slots__ = ("namespace",)

    @abstractmethod
    def with_namespace(self, namespace: str) -> Self:
        raise NotImplementedError
