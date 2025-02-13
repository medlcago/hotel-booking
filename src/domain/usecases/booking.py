from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from schemas.response import PaginationResponse

if TYPE_CHECKING:
    from schemas.booking import (
        BookingCreateRequest,
        BookingCancelRequest,
        BookingParams,
        BookingResponse,
        BookingPaymentResponse
    )


class IBookingUseCase(ABC):
    @abstractmethod
    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingPaymentResponse:
        raise NotImplementedError

    @abstractmethod
    async def cancel_booking(self, schema: BookingCancelRequest, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def confirm_booking(self, booking_id: int, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_bookings(self, user_id: int, params: BookingParams) -> PaginationResponse[BookingResponse]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_booking(self, booking_id: int, user_id: int) -> BookingResponse:
        raise NotImplementedError

    @abstractmethod
    async def cancel_pending_booking(self, booking_id: int, user_id: int) -> None:
        raise NotImplementedError
