from typing import Protocol

from schemas.booking import (
    BookingCreateRequest,
    BookingResponse,
    BookingCreateResponse,
    BookingParams,
    BookingCancelRequest
)
from schemas.response import PaginationResponse
from .booking_use_case import BookingUseCase


class IBookingUseCase(Protocol):
    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingCreateResponse:
        ...

    async def cancel_booking(self, schema: BookingCancelRequest, user_id: int) -> None:
        ...

    async def get_bookings(self, user_id: int, params: BookingParams) -> PaginationResponse[BookingResponse]:
        ...

    async def get_booking(self, booking_id: int, user_id: int) -> BookingResponse:
        ...
