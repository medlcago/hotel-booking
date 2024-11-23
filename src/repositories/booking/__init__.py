from typing import Protocol

from models import Booking
from repositories.base import Result
from .booking_repo import BookingRepository


class IBookingRepository(Protocol):
    async def get_user_bookings(self, user_id: int, **kwargs) -> Result[Booking]:
        ...
