from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, PositiveInt, Field

from schemas.filters import LimitOffset, OrderBy, SortOrderType


class ReviewParams(LimitOffset, OrderBy):
    hotel_id: Annotated[PositiveInt | None, Field(description="Сортировка по отелю")] = None
    field: str = "created_at"
    sort_order: SortOrderType = "desc"


class ReviewCreateRequest(BaseModel):
    hotel_id: PositiveInt
    score: Annotated[int, Field(ge=1, le=5)]
    comment: Annotated[str | None, Field(min_length=1, max_length=255)] = None


class ReviewCreateResponse(ReviewCreateRequest):
    id: PositiveInt
    user_id: PositiveInt
    created_at: datetime
    updated_at: datetime


class ReviewResponse(ReviewCreateResponse):
    pass
