from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.booking import (
        BookingCreateRequest,
        BookingResponse,
        BookingCreateResponse,
        BookingParams
    )
    from schemas.response import PaginationResponse


class IBookingService(ABC):
    @abstractmethod
    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingCreateResponse:
        raise NotImplementedError

    @abstractmethod
    async def cancel_booking(self, booking_id: int, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def confirm_booking(self, booking_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_bookings(self, user_id: int, params: BookingParams) -> PaginationResponse[BookingResponse]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_booking(self, booking_id: int, user_id: int) -> BookingResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_booking(self, booking_id: int) -> BookingResponse:
        raise NotImplementedError

    @abstractmethod
    async def cancel_pending_booking(self, booking_id: int) -> None:
        raise NotImplementedError
