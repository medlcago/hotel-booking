from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import date
    from models import Booking
    from repositories.base import Result


class IBookingRepository(ABC):
    @abstractmethod
    async def create_booking(self, values: dict[str, Any]) -> Booking:
        raise NotImplementedError

    @abstractmethod
    async def update_booking(self, booking_id: int, values: dict[str, Any]) -> Booking | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_bookings(
            self,
            user_id: int,
            limit: int,
            offset: int,
            **kwargs
    ) -> Result[Booking]:
        raise NotImplementedError

    @abstractmethod
    async def get_room_booking(self, room_id: int, date_from: date, date_to: date) -> Booking | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_booking(self, booking_id: int, user_id: int) -> Booking | None:
        raise NotImplementedError

    @abstractmethod
    async def get_booking(self, booking_id: int) -> Booking | None:
        raise NotImplementedError
