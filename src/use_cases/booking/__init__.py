from typing import Protocol

from schemas.booking import BookingCreateRequest, BookingResponse, BookingCreateResponse
from schemas.pagination import PaginationResponse
from .booking_use_case import BookingUseCase


class IBookingUseCase(Protocol):
    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingCreateResponse:
        ...

    async def cancel_booking(self, booking_id: int, user_id: int) -> None:
        ...

    async def get_bookings(self, user_id: int) -> PaginationResponse[BookingResponse]:
        ...

    async def get_booking(self, booking_id: int, user_id: int) -> BookingResponse:
        ...
