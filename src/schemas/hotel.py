from typing import Annotated, Any

from pydantic import BaseModel, Field, EmailStr, PositiveInt, field_validator

from schemas.filters import LimitOffset, OrderBy, SortOrderType
from utils.validators import PhoneType


class HotelParams(LimitOffset, OrderBy):
    location: Annotated[str | None, Field(description="Сортировка по локации")] = None
    field: str = "rating"
    sort_order: SortOrderType = "desc"


class HotelCreateRequest(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=150)]
    location: Annotated[str, Field(min_length=1, max_length=300)]
    phone: PhoneType | None = None
    email: EmailStr | None = None
    description: Annotated[str | None, Field(min_length=1, max_length=500)] = None


class HotelCreateResponse(HotelCreateRequest):
    id: PositiveInt


class HotelUpdate(HotelCreateRequest):
    name: Annotated[str | None, Field(min_length=1, max_length=150)] = None
    location: Annotated[str | None, Field(min_length=1, max_length=300)] = None
    phone: Annotated[str | None, Field(min_length=1, max_length=20)] = None
    email: EmailStr | None = None
    description: Annotated[str | None, Field(min_length=1, max_length=500)] = None

    # noinspection PyNestedDecorators
    @field_validator("name", "location")
    @classmethod
    def validate_fields(cls, v: Any):
        if v is None:
            raise ValueError("field cannot be null")
        return v


class HotelResponse(HotelCreateResponse):
    rating: float
