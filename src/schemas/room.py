from datetime import date
from decimal import Decimal
from typing import Annotated, Any

from pydantic import BaseModel, PositiveInt, Field, model_validator, field_validator

from enums.room import RoomType
from schemas.filters import LimitOffset


class RoomParams(LimitOffset):
    hotel_id: Annotated[PositiveInt | None, Field(description="Сортировка по отелю")] = None
    date_from: date
    date_to: date
    room_type: Annotated[RoomType | None, Field(description="Сортировка по типу комнаты")] = None

    @model_validator(mode="after")
    def validate_date(self):
        if self.date_from < date.today():
            raise ValueError("date_from must be today or later")
        if self.date_from >= self.date_to:
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


class RoomUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=1, max_length=150)] = None
    room_type: RoomType | None = None
    price_per_day: Decimal | None = None
    description: Annotated[str | None, Field(min_length=1, max_length=500)] = None

    # noinspection PyNestedDecorators
    @field_validator("name", "room_type", "price_per_day")
    @classmethod
    def validate_fields(cls, v: Any):
        if v is None:
            raise ValueError("Invalid data")
        return v


class RoomResponse(RoomCreateResponse):
    pass
