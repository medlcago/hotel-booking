from typing import Generic

from pydantic import BaseModel

from core.types import ModelType


class PaginationResponse(BaseModel, Generic[ModelType]):
    count: int
    items: list[ModelType]


class Message(BaseModel):
    message: str
