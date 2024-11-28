from datetime import date
from typing import Protocol, Any

from models import Booking
from repositories.base import Result
from .booking_repo import BookingRepository


class IBookingRepository(Protocol):
    async def create_booking(self, values: dict[str, Any]) -> Booking:
        ...

    async def update_booking(self, booking_id: int, values: dict[str, Any]) -> Booking | None:
        ...

    async def get_user_bookings(
            self,
            user_id: int,
            limit: int,
            offset: int,
            **kwargs
    ) -> Result[Booking]:
        ...

    async def get_room_booking(self, room_id: int, date_from: date, date_to: date) -> Booking | None:
        ...

    async def get_user_booking(self, booking_id: int, user_id: int) -> Booking | None:
        ...
