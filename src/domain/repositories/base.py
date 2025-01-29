from typing import Generic, TypeVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class Repository(Generic[ModelType]):
    table: Type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
