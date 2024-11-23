from datetime import date, timedelta
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, PositiveInt, Field, FutureDate, model_validator

from enums.room import RoomType
from schemas.pagination import PaginationParams


class RoomParams(PaginationParams):
    hotel_id: Annotated[PositiveInt | None, Field(description="Сортировка по отелю")] = None
    date_from: date = Field(default_factory=lambda: date.today())
    date_to: FutureDate = Field(default_factory=lambda: date.today() + timedelta(days=1))
    room_type: Annotated[RoomType | None, Field(description="Сортировка по типу комнаты")] = None

    @model_validator(mode="after")
    def validate_date(self):
        if self.date_from > self.date_to:
            raise ValueError("date_from must be before date_to")
        return self


class RoomCreateRequest(BaseModel):
    hotel_id: PositiveInt
    name: Annotated[str, Field(min_length=1, max_length=150)]
    room_type: RoomType
    price_per_day: Decimal
    description: Annotated[str | None, Field(min_length=1, max_length=500)] = None


class RoomCreateResponse(RoomCreateRequest):
    id: PositiveInt


class RoomResponse(RoomCreateResponse):
    pass
