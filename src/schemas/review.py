from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, PositiveInt, Field

from schemas.pagination import PaginationParams


class ReviewParams(PaginationParams):
    sort_order: Annotated[Literal["asc", "desc"], Field(description="Сортировка по дате создания")] = "asc"
    hotel_id: Annotated[PositiveInt | None, Field(description="Сортировка по отелю")] = None


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
