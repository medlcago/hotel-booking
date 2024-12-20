from typing import Generic, TypeVar

from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class PaginationResponse(BaseModel, Generic[ModelType]):
    count: int
    items: list[ModelType]


class Message(BaseModel):
    message: str
