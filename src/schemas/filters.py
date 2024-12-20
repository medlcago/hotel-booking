from typing import Annotated, Literal

from pydantic import BaseModel, Field

SortOrderType = Literal["asc", "desc"]


class LimitOffset(BaseModel):
    limit: Annotated[int, Field(ge=1, le=10)] = 10
    offset: Annotated[int, Field(ge=0)] = 0


class OrderBy(BaseModel):
    field: str = "id"
    sort_order: SortOrderType = "asc"
