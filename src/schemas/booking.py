from decimal import Decimal

from pydantic import BaseModel


class BookingResponse(BaseModel):
    room_id: int
    user_id: int
    total_days: int
    price_per_day: Decimal
    total_cost: Decimal
