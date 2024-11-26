from typing import Annotated

from pydantic import BaseModel, Field

from core.types import SortOrderType


class LimitOffset(BaseModel):
    limit: Annotated[int, Field(ge=1, le=10)] = 10
    offset: Annotated[int, Field(ge=0)] = 0


class OrderBy(BaseModel):
    field: str = "id"
    sort_order: SortOrderType = "asc"
