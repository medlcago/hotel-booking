from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import Generic, TypeVar, Type, Sequence, Callable

from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class AlreadyExistsError(Exception):
    pass


@dataclass
class Result(Generic[ModelType]):
    count: int
    items: Sequence[ModelType]


class Repository(Generic[ModelType]):
    table: Type[ModelType]

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory
