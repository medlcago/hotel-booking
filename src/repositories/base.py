from dataclasses import dataclass
from typing import Generic, TypeVar, Type, Sequence

ModelType = TypeVar("ModelType")


class AlreadyExistsError(Exception):
    pass


@dataclass
class Result(Generic[ModelType]):
    count: int
    items: Sequence[ModelType]


class Repository(Generic[ModelType]):
    table: Type[ModelType]
