from typing import Generic, TypeVar, Type

from domain.entities.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class Repository(Generic[ModelType]):
    table: Type[ModelType]
