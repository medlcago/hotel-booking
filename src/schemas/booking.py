from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, PositiveInt, model_validator

from enums.status import PaymentStatus
from schemas.filters import LimitOffset


class BookingParams(LimitOffset):
    payment_status: PaymentStatus | None = None


class BookingCreateRequest(BaseModel):
    room_id: PositiveInt
    date_from: date
    date_to: date

    @model_validator(mode="after")
    def validate_date(self):
        if self.date_from < date.today():
            raise ValueError("date_from must be today or later")
        if self.date_from >= self.date_to:
            raise ValueError("date_from must be before date_to")
        return self


class BookingCreateResponse(BaseModel):
    id: PositiveInt
    user_id: PositiveInt
    room_id: PositiveInt
    date_from: date
    date_to: date
    total_days: PositiveInt
    price_per_day: Decimal
    total_cost: Decimal
    created_at: datetime
    updated_at: datetime
    payment_status: PaymentStatus


class BookingResponse(BookingCreateResponse):
    pass


class BookingCancelRequest(BaseModel):
    booking_id: PositiveInt
