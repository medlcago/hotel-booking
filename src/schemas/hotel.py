from typing import Annotated

import phonenumbers
from pydantic import BaseModel, Field, EmailStr, model_validator, PositiveInt

from core.types import SortOrderType
from schemas.filters import LimitOffset, OrderBy


class HotelParams(LimitOffset, OrderBy):
    location: Annotated[str | None, Field(description="Сортировка по локации")] = None
    field: str = "rating"
    sort_order: SortOrderType = "desc"


class HotelCreateRequest(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=150)]
    location: Annotated[str, Field(min_length=1, max_length=300)]
    phone: Annotated[str | None, Field(min_length=1, max_length=20)] = None
    email: EmailStr | None = None
    description: Annotated[str | None, Field(min_length=1, max_length=500)] = None

    @model_validator(mode="after")
    def validate_phone(self):
        if not self.phone:
            return self
        try:
            parsed_number = phonenumbers.parse(self.phone, region="RU")
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Invalid phone number")
            return self
        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format")


class HotelCreateResponse(HotelCreateRequest):
    id: PositiveInt


class HotelUpdateRequest(HotelCreateRequest):
    name: Annotated[str | None, Field(min_length=1, max_length=150)] = None
    location: Annotated[str | None, Field(min_length=1, max_length=300)] = None


class HotelResponse(HotelCreateResponse):
    rating: float
