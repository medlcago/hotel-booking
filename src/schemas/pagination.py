from typing import Annotated, TypeVar, Generic

from pydantic import BaseModel, Field

ModelType = TypeVar("ModelType", bound=BaseModel)


class PaginationResponse(BaseModel, Generic[ModelType]):
    count: int
    items: list[ModelType]


class PaginationParams(BaseModel):
    limit: Annotated[int, Field(ge=1)] = 10
    offset: Annotated[int, Field(ge=0)] = 0
